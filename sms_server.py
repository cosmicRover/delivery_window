'''
Massive thanks to https://dev.to/mraza007/sending-sms-using-python-jkd
'''

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from user_creds import UserCreds


class SmsServer:
    def __init__(self):
        self.creds = UserCreds()
        self.email = self.creds.getSmsEmail()
        self.password = self.creds.getSmsEmailPass()

        self.sms_gateway = self.creds.getPhoneNum()+self.creds.getMobileServiceProvider()

        self.smtp = "smtp.gmail.com"
        self.port = 587

    def executeSms(self):
        server = smtplib.SMTP(self.smtp, self.port)

        # start server
        server.starttls()
        server.login(self.email, self.password)

        # compose message
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = self.sms_gateway
        msg['Subject'] = "Found delivery slot!!\n"
        body = "Come to the computer ASAP\n"

        # attach message
        msg.attach(MIMEText(body, 'plain'))
        sms = msg.as_string()

        # send message
        server.sendmail(self.email, self.sms_gateway, sms)

        # quit the server
        server.quit()
