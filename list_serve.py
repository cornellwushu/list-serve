import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
from dotenv import load_dotenv
from datetime import date, timedelta
from math import ceil
import sys

WUSHU_MEMBERS = []
with open("./members-wushu-l.csv", "r") as file:
    br = file.readlines()
    for email in br:
        WUSHU_MEMBERS.append(str(email.split(",")[11]))

load_dotenv()


class WushuEmail:
    def __init__(self, gmail_username, gmail_password, type):
        self.gmail_username = gmail_username
        self.gmail_password = gmail_password
        self.email_message = self.create_email_msg()
        self.type = type
        self.design_email_from_template()
        self.attach_images()

    def create_email_msg(self):
        msg = MIMEMultipart("alternative")
        return msg

    def design_email_from_template(self):
        now = date.today()
        monday = now - timedelta(days=now.weekday())
        thursday = monday + timedelta(days=3)
        friday = monday + timedelta(days=4)
        saturday = monday + timedelta(days=5)
        sunday = monday + timedelta(days=6)
        mondayDayMonth = str(monday.month) + "/" + str(monday.day)
        thursdayDayMonth = str(thursday.month) + "/" + str(thursday.day)
        fridayDayMonth = str(friday.month) + "/" + str(friday.day)
        saturdayDayMonth = str(saturday.month) + "/" + str(saturday.day)
        sundayDayMonth = str(sunday.month) + "/" + str(sunday.day)
        self.email_message["Subject"] = "Cornell Wushu Week of {}/{}!".format(
            monday.month, monday.day
        )
        self.email_message["From"] = "cornellwushu@gmail.com"
        self.email_message["To"] = "cornellwushu@gmail.com"
        html = open(f"./templates/{self.type}.html", "r").read()
        html = html.replace("{{ monday }}", mondayDayMonth)
        html = html.replace("{{ thursday }}", thursdayDayMonth)
        html = html.replace("{{ friday }}", fridayDayMonth)
        html = html.replace("{{ saturday }}", saturdayDayMonth)
        html = html.replace("{{ sunday }}", sundayDayMonth)
        body = MIMEText(html, "html")
        self.email_message.attach(body)

    def attach_images(self):
        fpFB = open(".\images/facebook.png", "rb")
        fpIG = open(".\images/instagram.png", "rb")
        fpGC = open(".\images/google-calendar.png", "rb")
        fpWB = open(".\images/logo.jpg", "rb")
        fpYT = open(".\images/youtube.png", "rb")
        msgFB = MIMEImage(fpFB.read())
        msgIG = MIMEImage(fpIG.read())
        msgGC = MIMEImage(fpGC.read())
        msgWB = MIMEImage(fpWB.read())
        msgYT = MIMEImage(fpYT.read())
        fpFB.close()
        fpIG.close()
        fpGC.close()
        fpWB.close()
        fpYT.close()
        msgFB.add_header("Content-ID", "<facebook>")
        msgIG.add_header("Content-ID", "<instagram>")
        msgGC.add_header("Content-ID", "<google-calendar>")
        msgWB.add_header("Content-ID", "<website>")
        msgYT.add_header("Content-ID", "<youtube>")
        self.email_message.attach(msgFB)
        self.email_message.attach(msgIG)
        self.email_message.attach(msgGC)
        self.email_message.attach(msgWB)
        self.email_message.attach(msgYT)

    def send_email(self, receivers):
        num_receivers = len(receivers)
        for i in range(ceil(num_receivers / 100)):
            to = receivers[:100]
            smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
            smtp_server.starttls()
            smtp_server.login(self.gmail_username, self.gmail_password)
            smtp_server.sendmail(
                self.gmail_username, to, self.email_message.as_string()
            )
            smtp_server.close()
            try:
                receivers = receivers[100:]
            except:
                break
        print("Email Sent Succesfully!")


if __name__ == "__main__":
    email = WushuEmail(
        os.environ.get("GMAIL_USER"), os.environ.get("GMAIL_PASSWORD"), "weekly"
    )
    try:
        if sys.argv[1] == "testing":
            email.send_email(["ps2245@cornell.edu"])
        else:
            email.send_email(WUSHU_MEMBERS)
    except:
        email.send_email(WUSHU_MEMBERS)
