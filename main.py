import tempfile
from datetime import datetime, timedelta
from typing import Tuple

import jinja2
import os

import settings
from analytics import get_data, rolling_bands
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


def generate_report(stock: str, to_address: Tuple[str, str], **kwargs):
    end_date = kwargs.get('end_date', datetime.today().strftime('%Y-%m-%d'))
    start_date = datetime.today() - timedelta(days=90)
    start_date = start_date.strftime('%Y-%m-%d')
    start_date = kwargs.get('start_date', start_date)

    df = get_data([stock], start_date, end_date)
    rolling_bands_df = rolling_bands(df, column_name=stock)
    title = f'{stock} report {start_date}-{end_date}'
    dataframe_to_image(rolling_bands_df, TMP_FILENAME,
                       graph_title=title,
                       colors={stock: 'blue', 'Lower': 'red', 'Upper': 'red'})
    html = generate_report_html(title=title)
    send_report(html, to_address, subject=title)


if __name__ == '__main__':
    # html = generate_report_html(title='Stocks report')
    # send_report(html, settings.REPORT_RECIPIENT,
    #             subject='Stocks report')
    generate_report('AMZN', settings.REPORT_RECIPIENT)
