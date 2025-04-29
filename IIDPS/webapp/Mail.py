import os,sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def mailsend(toaddr,msgsub,msgbody):

    fromadrs="sajidprojects5@gmail.com"
    password = ""

    msg = MIMEMultipart()
    msg['From'] = fromadrs
    msg['To'] = toaddr
    msg['Subject'] = msgsub
    body = msgbody
    msg.attach(MIMEText(body, 'html'))


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo
    server.starttls()
    server.login(fromadrs, password)
    text = msg.as_string()
    server.sendmail(fromadrs, toaddr, text)
    server.quit()
    print("sent email")

if __name__ == '__main__':
    mailsend('sajidprojects5@gmail.com','subject','<h1>bodyyyyyyy<br>yyyyyy<font color=red>yyyyyyyyy<a href="https://google.com">yyyyyyyyyy</a>yyy')
