import logging
import smtplib
from email.message import EmailMessage

class EmailConfig():
    def __init__(self, account, passwd, server_addr, server_port):
        self.account = account
        self.passwd = passwd
        self.server_addr = server_addr
        self.server_port = server_port

def send_code(config, email_addr, code):
    server = smtplib.SMTP_SSL(config.server_addr, config.server_port)
    server.ehlo()
    server.login(config.account, config.passwd)
    msg = EmailMessage()
    msg.set_content(code)
    msg['Subject'] = "UBC Discord Access Code"
    msg['From'] = config.account
    msg['To'] = email_addr
    server.send_message(msg, config.account, email_addr)
    server.close() 
    logging.info(f"sent access code to {email_addr}") 
