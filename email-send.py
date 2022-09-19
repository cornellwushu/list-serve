"""
Steps to set up email-sender:
1)  Go to google account settings and enable two-step verification
2)  Go to app passwords and generate a new password for mail sending
3)  Use the generated password to login to the email 
"""
# TODO: Only a 100 people can receive email, so fix that
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
from datetime import date, timedelta


gmail_user = "cornellwushu@gmail.com"
gmail_password = "gkesxwbfpifgprek"

blockedAt = "zmj6@cornell.edu"
blockPassed = False
receivers = []
with open(
    "C:/Users\praty\Desktop\cornell-wushu\list-serve\members-wushu-l.csv", "r"
) as file:
    br = file.readlines()
    for email in br:
        if blockPassed:
            receivers.append(str(email.split(",")[11]))
        elif str(email.split(",")[11]) == blockedAt:
            blockPassed = True
print("commit")


sent_from = gmail_user
to = ["ps2245@cornell.edu"]
today = date.today()
friday = today + timedelta(days=4)
saturday = today + timedelta(days=5)
mondayDayMonth = str(today.month) + "/" + str(today.day)
fridayDayMonth = str(friday.month) + "/" + str(friday.day)
saturdayDayMonth = str(saturday.month) + "/" + str(saturday.day)
msg = MIMEMultipart("alternative")
msg["Subject"] = "Cornell Wushu Week of {}/{}!".format(today.month, today.day)
msg["From"] = "cornellwushu@gmail.com"
msg["To"] = "cornellwushu@gmail.com"

fpGIF = open(
    "C:/Users\praty\Desktop\cornell-wushu\cornell-wushu\src\images\wushu.gif", "rb"
)
fpFB = open("C:/Users\praty\Desktop\cornell-wushu\list-serve\\facebook.png", "rb")
fpIG = open("C:/Users\praty\Desktop\cornell-wushu\list-serve\instagram.png", "rb")
fpGC = open("C:/Users\praty\Desktop\cornell-wushu\list-serve\google-calendar.png", "rb")
fpWB = open("C:/Users\praty\Desktop\cornell-wushu\list-serve\logo.jpg", "rb")
fpYT = open("C:/Users\praty\Desktop\cornell-wushu\list-serve\youtube.png", "rb")
fpPF = open(
    "C:/Users\praty\Desktop\cornell-wushu\list-serve\performance-image.jpeg", "rb"
)
msgGIF = MIMEImage(fpGIF.read())
msgFB = MIMEImage(fpFB.read())
msgIG = MIMEImage(fpIG.read())
msgGC = MIMEImage(fpGC.read())
msgWB = MIMEImage(fpWB.read())
msgYT = MIMEImage(fpYT.read())
msgPF = MIMEImage(fpPF.read())
fpGIF.close()
fpFB.close()
fpIG.close()
fpGC.close()
fpWB.close()
fpYT.close()
fpPF.close()
msgGIF.add_header("Content-ID", "<gif>")
msgFB.add_header("Content-ID", "<facebook>")
msgIG.add_header("Content-ID", "<instagram>")
msgGC.add_header("Content-ID", "<google-calendar>")
msgWB.add_header("Content-ID", "<website>")
msgYT.add_header("Content-ID", "<youtube>")
msgPF.add_header("Content-ID", "<performance>")
msg.attach(msgGIF)
msg.attach(msgFB)
msg.attach(msgIG)
msg.attach(msgGC)
msg.attach(msgWB)
msg.attach(msgYT)
msg.attach(msgPF)

# Create the body of the message (a plain-text and an HTML version).
html = open("template.html", "r").read()
html = html.replace("{{ monday }}", mondayDayMonth)
html = html.replace("{{ friday }}", fridayDayMonth)
html = html.replace("{{ saturday }}", saturdayDayMonth)

# part1 = MIMEText(text, "plain")
body = MIMEText(html, "html")

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
# msg.attach(part1)
msg.attach(body)
smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
smtp_server.starttls()
smtp_server.login(gmail_user, gmail_password)
smtp_server.sendmail(sent_from, to, msg.as_string())
smtp_server.close()
print("Email sent successfully!")
