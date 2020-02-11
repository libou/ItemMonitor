from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import sys
from email.mime.text import MIMEText
from email.header import Header
import smtplib
from random import randint
import time
import logging
import os


def RomanticCrown(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urlopen(req).read()
    except Exception as e:
        msg = """
          <p>获取货品信息错误</p>
          <a href="{}">货品链接</a>
          """.format(url)
        logging.error("Obtaining Item Info Error: {}".format(e))
        return msg

    try:
        html_soup = BeautifulSoup(response, "html.parser")
        size_container = html_soup.optgroup
        size_m = size_container.find('option', attrs={'value': 'P0000EDP000B'})
        if size_m is None:
            msg = """
            <p>获取货品信息错误</p>
            <a href="{}">货品链接</a>
            """.format(url)
            return msg
        if "out of stock" in size_m.text:
            logging.info("Item No Change")
            return False
        else:
            msg = """
            <p>货品状态更新</p>
            <a href="{}">货品链接</a>
            """.format(url)
            logging.warning("Item State Changed")
            return msg
    except Exception as e:
        msg = """
                       <p>获取货品信息错误</p>
                       <a href="{}">货品链接</a>
                       """.format(url)
        logging.error("Obtaining Item Info Error: {}".format(e))
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
        logging.info("Notification sended successfully")
    except smtplib.SMTPException as e:
        print(e)
        logging.error("Error: Sending Notification - {}".format(e))


def main(sender, pw, receiver):
    logging.info("ItemMonitor running")
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

    if not os.path.exists("log"):
        os.mkdir("log")

    logging.basicConfig(level=logging.INFO,
                        filename='log/moniter.log',
                        format=
                        '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                        )
    logging.info("ItemMonitor launching")
    main(sender, pw, receiver)



