import time
from datetime import datetime as dt

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

from user_creds import UserCreds
from sms_server import SmsServer


class BrowserDriver:
    # data prep from the UserCreds class
    def __init__(self):
        creds = UserCreds()
        self.email = creds.getEmail()
        self.password = creds.getPass()
        self.ukey = creds.getUniqueKey()
        self.wday = creds.getWatchDate()
        self.getPhoneNumber = creds.getPhoneNum()
        self.xPathDict = {
            'url': 'http://www.amazon.com/',
            'nav': '//*[@id="nav-link-accountList"]',
            'email': '//*[@id="ap_email"]',
            'continue': '//*[@id="continue"]',
            'pass': '//*[@id="ap_password"]',
            'submit': '//*[@id="signInSubmit"]',
            'cart': '//*[@id="nav-cart"]',
            'fresh': '//*[@id="sc-alm-buy-box-ptc-button-' + self.ukey + '"]/span/input',
            'final_continue': '//*[@id="a-autoid-0"]/span/a',
            'attended': '//*[@id="servicetype-selector-button-attended-announce"]',
            'watch_day': '//*[@id="date-button-' + self.wday + '-announce"]'
        }
        self.cssDict = {
            'slot': '#slot-container-ATTENDED > div > div > div > span',
        }

        # configure webdrive accroding to platform
        self.browser = webdriver.Chrome(creds.getUserPlatform())

    def findInputFieldByXpathAndPopulate(self, xpath, value):
        field = self.browser.find_element_by_xpath(xpath)
        field.send_keys(value)

    def findByXpathAndClick(self, xpath):
        self.browser.find_element_by_xpath(xpath).click()

    def waitDriver(self, time, xpath):
        ignored_exceptions = (NoSuchElementException,
                              StaleElementReferenceException,)
        wait = WebDriverWait(self.browser, time)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        button.click()

    def launchUrl(self, url):
        self.browser.get(url)

    def getDeleiverySlotStatus(self):
        status = self.browser.find_elements_by_css_selector(
            self.cssDict['slot'])

        results = []

        for x in status:
            results.append(x.text)

        return any(e for e in results if e.startswith("No attended delivery windows are available for"))

    def watchForSlots(self):
        self.waitDriver(
            10.0, self.xPathDict['attended'])
        self.waitDriver(
            10.0, self.xPathDict['watch_day'])
        print(dt.now())

    def sendSms(self):
        print("sending sms")
        sms = SmsServer()
        sms.executeSms()

    def executeWatch(self):
        self.launchUrl(self.xPathDict['url'])
        self.waitDriver(10.0, self.xPathDict['nav'])
        self.waitDriver(10.0, self.xPathDict['email'])
        self.findInputFieldByXpathAndPopulate(self.xPathDict['email'], self.email)
        self.waitDriver(10.0, self.xPathDict['continue'])
        self.findInputFieldByXpathAndPopulate(self.xPathDict['pass'], self.password)
        self.waitDriver(10.0, self.xPathDict['submit'])
        self.waitDriver(10.0, self.xPathDict['cart'])
        self.waitDriver(10.0, self.xPathDict['fresh'])
        self.waitDriver(10.0, self.xPathDict['final_continue'])
        self.waitDriver(10.0, self.xPathDict['attended'])

        self.watchForSlots()

        # loop until a delivery window is available
        isUnAvailable = self.getDeleiverySlotStatus()
        while isUnAvailable:
            print("searching for a slot")
            time.sleep(60) #refresh time in seconds
            self.browser.refresh()
            self.watchForSlots()
            isUnAvailable = self.getDeleiverySlotStatus()
        else:
            print("found window!!!!")
            self.sendSms()

        print("program is finished!")


if __name__ == "__main__":
    wd = BrowserDriver()
    wd.executeWatch()
