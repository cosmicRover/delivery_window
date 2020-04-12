class UserCreds:
    '''
    [step0]
    ******** make sure you have python3 and pip installed: run(mac/linux) -> sudo pip install selenium 
    *** for windows -> https://www.liquidweb.com/kb/install-pip-windows/ the run pip install selenium
    '''

    '''
    [step1]
    configure your os i.e. mac, linux, windows
    '''
    def myOs(self):
        return 'mac'

    def getUserPlatform(self):
        return 'chrome_'+self.myOs()+'/chromedriver'

    '''
    [step2]
    Amazon email and passwords
    '''

    def getEmail(self):
        return 'your_amazon_email'

    def getPass(self):
        return 'your_amazon_pass'

    '''
    [step3]
    To get this unique key: 
    1. put something on your amazon fresh cart
    2. On chrome, right click, inspect on *amazon fresh* yellow checkout button
    3. You will see "proceedToAlmCheckout-your_unique_key_is_here".
    4. Grab the key and paste it down below.
    '''

    def getUniqueKey(self):
        return 'your_amazon_fresh_unique_key'

    '''
    [step4]
    The date you want to watch for
    format the date to: YYYY-MM-DD i.e: '2020-04-14'
    '''

    def getWatchDate(self):
        return 'your_watch_date'

    '''
    [step5]
    The phone number you would like to receive SMS notifications on
    '''

    def getPhoneNum(self):
        return 'your_phone_number'

    '''
    [step6]
    Supported providers. Pick your provider from here:
    AT&T: @txt.att.net
    Sprint: @messaging.sprintpcs.com or @pm.sprint.com
    T-Mobile: @tmomail.net
    Verizon: @vtext.com
    Boost Mobile: @myboostmobile.com
    Cricket: @sms.mycricket.com
    Metro PCS: @mymetropcs.com
    Tracfone: @mmst5.tracfone.com
    U.S. Cellular: @email.uscc.net
    Virgin Mobile: @vmobl.com
    '''

    def getMobileServiceProvider(self):
        return 'your_phone_service_provider'

    '''
    [step7]
    Since I tested on gmail, I had to turn on Imap on the settings and then,
    turn on "Less Secure app access" via the account's security page. I'll include a helpful video tutorial below
    https://www.youtube.com/watch?v=D-NYmDWiFjU
    Below takes in your account email and pass. You can use a throwaway email for this provided that you enable imap and turn
    on less secure apps.
    '''

    def getSmsEmail(self):
        return "your_email"

    def getSmsEmailPass(self):
        return "your_pass"
