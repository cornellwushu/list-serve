import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
from datetime import date, timedelta
from math import ceil

WUSHU_MEMBERS = []
with open("\members-wushu-l.csv", "r") as file:
    br = file.readlines()
    for email in br:
        WUSHU_MEMBERS.append(str(email.split(",")[11]))

gmail_user = "cornellwushu@gmail.com"
gmail_password = "gkesxwbfpifgprek"


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
        today = date.today()
        friday = today + timedelta(days=4)
        saturday = today + timedelta(days=5)
        mondayDayMonth = str(today.month) + "/" + str(today.day)
        fridayDayMonth = str(friday.month) + "/" + str(friday.day)
        saturdayDayMonth = str(saturday.month) + "/" + str(saturday.day)
        self.msg["Subject"] = "Cornell Wushu Week of {}/{}!".format(
            today.month, today.day
        )
        self.msg["From"] = "cornellwushu@gmail.com"
        self.msg["To"] = "cornellwushu@gmail.com"
        html = open(f"\templates\{self.type}.html", "r").read()
        html = html.replace("{{ monday }}", mondayDayMonth)
        html = html.replace("{{ friday }}", fridayDayMonth)
        html = html.replace("{{ saturday }}", saturdayDayMonth)
        body = MIMEText(html, "html")
        self.email_message.attach(body)

    def attach_images(self):
        fpGIF = open(
            "C:/Users\praty\Desktop\cornell-wushu\cornell-wushu\src\images\wushu.gif",
            "rb",
        )
        fpFB = open("images\facebook.png", "rb")
        fpIG = open("images\instagram.png", "rb")
        fpGC = open("images\google-calendar.png", "rb")
        fpWB = open("images\logo.jpg", "rb")
        fpYT = open("images\youtube.png", "rb")
        msgGIF = MIMEImage(fpGIF.read())
        msgFB = MIMEImage(fpFB.read())
        msgIG = MIMEImage(fpIG.read())
        msgGC = MIMEImage(fpGC.read())
        msgWB = MIMEImage(fpWB.read())
        msgYT = MIMEImage(fpYT.read())
        fpGIF.close()
        fpFB.close()
        fpIG.close()
        fpGC.close()
        fpWB.close()
        fpYT.close()
        msgGIF.add_header("Content-ID", "<gif>")
        msgFB.add_header("Content-ID", "<facebook>")
        msgIG.add_header("Content-ID", "<instagram>")
        msgGC.add_header("Content-ID", "<google-calendar>")
        msgWB.add_header("Content-ID", "<website>")
        msgYT.add_header("Content-ID", "<youtube>")
        self.email_message.attach(msgGIF)
        self.email_message.attach(msgFB)
        self.email_message.attach(msgIG)
        self.email_message.attach(msgGC)
        self.email_message.attach(msgWB)
        self.email_message.attach(msgYT)

    def send_email(self, receivers):
        num_receivers = len(receivers)
        for i in range(ceil(num_receivers / 100)):
            to = receivers[:99]
            smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
            smtp_server.starttls()
            smtp_server.login(self.gmail_usernamer, self.gmail_password)
            smtp_server.sendmail(
                self.gmail_username, to, self.email_message.as_string()
            )
            smtp_server.close()
            receivers = receivers[99:]


if __name__ == "__main__":
    email = WushuEmail(gmail_user, gmail_password, "social")
    testing = True
    if testing:
        email.send_email(["ps2245@cornell.edu"])
    else:
        email.send_email(WUSHU_MEMBERS)
