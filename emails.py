import os
import smtplib, ssl
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from typing import List, Tuple

import jinja2

import settings

IMAGE_EXTENSIONS = (
    '.ras', '.xwd', '.bmp', '.jpe', '.jpg', '.jpeg', '.xpm', '.ief', '.pbm', '.tif', '.gif', '.ppm', '.xbm', '.tiff',
    '.rgb', '.pgm', '.png', '.pnm')


class EmailSender(object):

    def __init__(self, smtp_server: str, port: int, user: str, password: str):
        context = ssl.create_default_context()
        self._server = smtplib.SMTP_SSL(smtp_server, port, context=context)
        # self._server.set_debuglevel(1)
        self._server.login(user, password)

    def send_email(self, from_addr: Tuple[str, str], to_addr: Tuple[str, str], subject: str, html: str,
                   attachments: List[str] = []):
        """
        Send an email
        :param from_addr: Tuple of (sender name, sender email)
        :param to_addr: Tuple of (receiver name, receiver email)
        :param subject: Email subject
        :param html: html text of email
        :param attachments: List of attachments to include in email
        """
        msg = MIMEMultipart()
        msg['From'] = EmailSender._re_format_addr('%s <%s>' % (from_addr[0], from_addr[1]))
        msg['To'] = EmailSender._re_format_addr('%s <%s>' % (to_addr[0], to_addr[1]))
        msg['Subject'] = Header(subject, 'utf-8').encode()

        html_part = MIMEText(html, 'html', 'utf-8')
        msg.attach(html_part)

        for ind, attachment in enumerate(attachments):
            ext = os.path.splitext(attachment)[-1].lower()
            if ext in IMAGE_EXTENSIONS:
                mime = EmailSender._generate_image_mime(attachment, ind)
            else:
                f = open(attachment, 'rb')
                mime = MIMEBase("application", "octet-stream")
                mime.set_payload(f.read())
            encoders.encode_base64(mime)
            msg.attach(mime)
        self._server.sendmail(from_addr[1], to_addr[1], msg.as_string())

    def close(self):
        self._server.close()

    @staticmethod
    def _re_format_addr(email: str):
        """
        parse email to get user real name and email address.
        :param email: String with format "name of sender <name@email.com>"
        :return:
        """
        name, addr = parseaddr(email)
        name_encoded = Header(name, 'utf-8').encode()
        return formataddr((name_encoded, addr))

    @staticmethod
    def _generate_image_mime(filepath: str, attachment_index: int) -> MIMEBase:
        """
        Generate a Mime attachment for image type
        :param filepath: image file
        :param attachment_index: attachment index (so it can be included in html msg)
        :return: MimeBase of image
        """
        f = open(filepath, 'rb')
        ext = os.path.splitext(filepath)[-1].lower()
        filepath_array = filepath.split('/')
        mime = MIMEBase('image', ext, filename=filepath_array[-1])
        mime.add_header('Content-Disposition', 'attachment', filename=filepath_array[-1])
        mime.add_header('X-Attachment-Id', f'{attachment_index}')
        mime.add_header('Content-ID', f'<{attachment_index}>')
        mime.set_payload(f.read())
        return mime


if __name__ == '__main__':
    email_sender = EmailSender("smtp.gmail.com", 465, settings.SMTP_SERVER_USER, settings.SMTP_SERVER_PASSWORD)
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    html_template = template_env.get_template(settings.REPORT_TEMPLATE)
    html = html_template.render()
    email_sender.send_email(("a", "a@gmail.com"),
                            ("b", "style.daniel@gmail.com"),
                            "subject",
                            html)
