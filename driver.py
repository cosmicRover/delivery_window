import time

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
    #data prep from the UserCreds class
    def __init__(self):
        creds = UserCreds()
        self.email = creds.getEmail()
        self.password = creds.getPass()
        self.ukey = creds.getUniqueKey()
        self.wday = creds.getWatchDate()
        self.getPhoneNumber = creds.getPhoneNum()

        #configure webdrive accroding to platform
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
            "#slot-container-ATTENDED > div > div > div > span")
        return status[2].text

    def watchForSlots(self):
        self.waitDriver(
            10.0, '//*[@id="servicetype-selector-button-attended-announce"]')
        self.waitDriver(10.0, '//*[@id="date-button-'+ self.wday + '-announce"]')

    def sendSms(self):
        print("sending sms")
        sms = SmsServer()
        sms.executeSms()

    def executeWatch(self):
        self.launchUrl('http://www.amazon.com/')
        self.waitDriver(10.0, '//*[@id="nav-link-accountList"]')
        self.findInputFieldByXpathAndPopulate(
            '//*[@id="ap_email"]', self.email)
        self.waitDriver(10.0, '//*[@id="continue"]')
        self.findInputFieldByXpathAndPopulate(
            '//*[@id="ap_password"]', self.password)
        self.waitDriver(10.0, '//*[@id="signInSubmit"]')
        self.waitDriver(10.0, '//*[@id="nav-cart"]')
        self.waitDriver(
            10.0, '//*[@id="sc-alm-buy-box-ptc-button-'+ self.ukey + '"]/span/input')
        self.waitDriver(10.0, '//*[@id="a-autoid-0"]/span/a')
        self.watchForSlots()

        #loop until a delivery window is available
        status = self.getDeleiverySlotStatus()
        while "No attended delivery windows are available for" in status:
            print(status)
            time.sleep(5)
            self.browser.refresh()
            self.watchForSlots()
            status = self.getDeleiverySlotStatus()
        else:
            print("found window!!!!")
            self.sendSms()

        print("program is finished!")


if __name__ == "__main__":
    wd = BrowserDriver()
    wd.executeWatch()
