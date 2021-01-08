import base64
import logging
import smtplib
from typing import *
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from models.screenshot import Screenshot


logger = logging.getLogger(__name__)

class EmailHtmlMessage:

    def __init__(self, smtp_server : str, smtp_port : int, smtp_user : Optional[str], smtp_pass : Optional[str]) -> None:

        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass

    def send_email(self, receipients : List[str], sender : str, subject : str, html : str, images : Iterable[Screenshot] = []) -> None:

        logger.info('Building email message')

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = ", ".join(receipients)

        part = MIMEText(html, "html")
        message.attach(part)

        logger.info("Attaching inline images")
        for image in images:
            msgImage = MIMEImage(base64.decodebytes(image.b64png.encode()))
            msgImage.add_header('Content-ID', f'<{image.cid}>')
            message.attach(msgImage)

        logger.info('Sending email')

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:

            if self.smtp_user and self.smtp_pass:
                server.login(self.smtp_user, self.smtp_pass)

            server.sendmail(sender, receipients, message.as_string())

        logger.info('Email sent')

