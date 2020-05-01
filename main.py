import tempfile
from typing import Tuple

import jinja2
import os

import settings
from emails import EmailSender
from generate_graph import dataframe_to_image, generate_report_from_csv_str

TEMP_DIR = tempfile.gettempdir()
TMP_FILENAME = os.path.join(TEMP_DIR, 'graph.png')


def generate_report_html(**kwargs):
    title = kwargs.get('title', settings.REPORT_SUBJECT)
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    html_template = template_env.get_template(settings.REPORT_TEMPLATE)
    html = html_template.render(
        title=title
    )
    return html


def send_report(content: str, to: Tuple[str, str], **kwargs):
    """

    :param to   Tuple of (receiver name, receiver email)
    :return:
    """
    subject = kwargs.get('subject', settings.REPORT_SUBJECT)
    from_address = kwargs.get('from', settings.REPORT_SENDER)
    graph_attachment = kwargs.get('attachment', TMP_FILENAME)
    email_sender = EmailSender(settings.SMTP_SERVER,
                               settings.SMTP_SERVER_PORT,
                               settings.SMTP_SERVER_USER,
                               settings.SMTP_SERVER_PASSWORD)
    email_sender.send_email(from_address,
                            to,
                            subject,
                            content,
                            attachments=[graph_attachment])
    os.remove(TMP_FILENAME)


if __name__ == '__main__':
    html = generate_report_html(title='Stocks report')
    send_report(html, settings.REPORT_RECIPIENT,
                subject='Stocks report')
