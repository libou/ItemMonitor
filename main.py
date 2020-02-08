from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import sys
from email.mime.text import MIMEText
from email.header import Header
import smtplib
from random import randint
import time


def RomanticCrown(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req).read()

    html_soup = BeautifulSoup(response, "html.parser")
    if html_soup is None:
        msg = """
               <p>获取货品信息错误</p>
               <a href="{}">货品链接</a>
               """.format(url)
        return msg
    size_container = html_soup.optgroup
    if size_container is None:
        msg = """
               <p>获取货品信息错误</p>
               <a href="{}">货品链接</a>
               """.format(url)
        return msg
    size_m = size_container.find('option', attrs={'value': 'P0000EDP000B'})
    if size_m is None:
        msg = """
        <p>获取货品信息错误</p>
        <a href="{}">货品链接</a>
        """.format(url)
        return msg
    if "out of stock3" in size_m.text:
        return False
    else:
        msg = """
        <p>货品状态更新</p>
        <a href="{}">货品链接</a>
        """.format(url)
        return msg

def Notification(sender, pw, receiver, content):
    mail_host = "smtp.163.com"

    # Email Notification
    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = "Item State Notification"

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(sender, pw)
        smtpObj.sendmail(sender, receiver, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)


def main(sender, pw, receiver):
    while True:
        # RomanticCrown Monitor
        url = 'https://global.romanticcrown.com/product/inuit-corduroy-down-parkaoatmeal/2797/?cate_no=36&display_group=1'
        result = RomanticCrown(url)
        if result:
            Notification(sender, pw, receiver, result)
        time.sleep(randint(15, 60) * 60)



if __name__ == '__main__':
    sender = sys.argv[1]
    pw = sys.argv[2]
    receiver = sys.argv[3]
    main(sender, pw, receiver)



