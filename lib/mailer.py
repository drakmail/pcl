# -*- coding: utf-8 -*-

# Mailer library.
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from lib import common

class Mailer:
    def __init__(self):
        self.config = common.SETTINGS

        self.mail_from = self.config["mailer"]["send_from"]
        self.smtp_host = self.config["smtp"]["smtp_host"]
        self.smtp_username = self.config["smtp"]["smtp_username"]
        self.smtp_password = self.config["smtp"]["smtp_password"]
        self.smtp_tls = self.config["smtp"]["smtp_tls"]
        self.smtp_ssl = self.config["smtp"]["smtp_ssl"]

    def process_mail(self, recipient, subject, mail_text):
        """
        Sends an email.
        """
        self.mail_text = mail_text
        self.recipient = recipient
        self.subject = subject
        if self.config["mailer"]["mail_mode"] == "sendmail":
            self.send_with_sendmail()
        elif self.config["mailer"]["mail_mode"] == "smtp":
            self.send_with_smtp()

    def send_with_sendmail(self):
        """
        Send mail with sendmail.
        """
        p = os.popen("/usr/sbin/sendmail -t", "w")
        p.write("From: {0}\n".format(self.mail_from))
        p.write("To: {0}\n".format(self.recipient))
        p.write("Subject: {0}\n".format(self.subject))
        p.write("Content-Type: text/plain; charset=utf-8\n")
        p.write("\n")
        p.write(self.mail_text)
        retcode = p.close()
        if retcode:
            print("Failed to send message with sendmail!")

    def send_with_smtp(self):
        """
        Send mail with SMTP.
        """
        message = MIMEMultipart()
        message.set_charset("utf-8")
        message["FROM"] = self.mail_from
        message["Subject"] = self.subject
        message["To"] = self.recipient
        message.attach(MIMEText(self.mail_text, "plain", "UTF-8"))

        server = smtplib.SMTP(self.smtp_host)
        server.starttls()
        server.login(self.smtp_username, self.smtp_password)
        server.sendmail(self.mail_from, self.recipient, message.as_string())
        server.quit()