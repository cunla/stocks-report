import tempfile
from datetime import datetime, timedelta
from typing import Tuple, List
import numpy as np
import pandas as pd

import jinja2
import os

import settings
from analytics import get_data, rolling_bands
from emails import EmailSender
from generate_graph import dataframe_to_image, generate_report_from_csv_str

TEMP_DIR = tempfile.gettempdir()
TMP_FILENAME = os.path.join(TEMP_DIR, 'graph.png')


def generate_report_html(start_date, end_date, **kwargs):
    title = kwargs.get('title', settings.REPORT_SUBJECT)
    portfolio = kwargs.get('portfolio', None)
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    html_template = template_env.get_template(settings.REPORT_TEMPLATE)
    html = html_template.render(
        title=title,
        portfolio=portfolio,
        start_date=start_date,
        end_date=end_date,
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


def generate_stock_report(stock: str, to_address: Tuple[str, str], **kwargs):
    end_date = kwargs.get('end_date', datetime.today().strftime('%Y-%m-%d'))
    start_date = datetime.today() - timedelta(days=90)
    start_date = start_date.strftime('%Y-%m-%d')
    start_date = kwargs.get('start_date', start_date)

    df = get_data([stock], start_date, end_date)
    df.dropna(inplace=True)
    rolling_bands_df = rolling_bands(df, column_name=stock)
    title = f'{stock} report {start_date}-{end_date}'
    dataframe_to_image(rolling_bands_df, TMP_FILENAME,
                       graph_title=title,
                       colors={stock: 'blue', 'Lower': 'red', 'Upper': 'red'})
    html = generate_report_html(title=title,
                                start_date=start_date,
                                end_date=end_date)
    send_report(html, to_address, subject=title)


def generate_portfolio_report(portfolio: List[Tuple[float, str]],
                              start_date: datetime,
                              end_date: datetime) -> pd.DataFrame:
    stocks = [item[1] for item in portfolio]
    percentage = np.array([item[0] for item in portfolio])
    res_df = get_data(stocks, start_date, end_date)
    res_df.dropna(inplace=True)
    res_df['portfolio'] = res_df.values.dot(percentage)
    return res_df


def send_portfolio_report(portfolio: List[Tuple[float, str]],
                          to_address: Tuple[str, str],
                          **kwargs):
    end_date = kwargs.get('end_date', datetime.today().strftime('%Y-%m-%d'))
    start_date = datetime.today() - timedelta(days=90)
    start_date = start_date.strftime('%Y-%m-%d')
    start_date = kwargs.get('start_date', start_date)

    portfolio_df = generate_portfolio_report(portfolio,
                                             start_date=start_date,
                                             end_date=end_date)
    rolling_bands_df = rolling_bands(portfolio_df, column_name='portfolio')
    portfolio_str = ' +'.join(f'{item[0] * 100}%*{item[1]}' for item in portfolio)
    title = f'Portfolio report {start_date}-{end_date}'
    dataframe_to_image(rolling_bands_df, TMP_FILENAME,
                       graph_title=title,
                       colors={'portfolio': 'blue', 'Lower': 'red', 'Upper': 'red'})
    html = generate_report_html(title=title,
                                start_date=start_date,
                                end_date=end_date,
                                portfolio=portfolio, )
    send_report(html, to_address, subject=title)


if __name__ == '__main__':
    # html = generate_report_html(title='Stocks report')
    # send_report(html, settings.REPORT_RECIPIENT,
    #             subject='Stocks report')
    # generate_stock_report('AMZN', settings.REPORT_RECIPIENT)
    portfolio = [(0.20, 'AMZN'),
                 (0.20, 'AAPL'),
                 (0.20, 'GOOG'),
                 (0.20, 'FB'),
                 (0.20, 'TSLA'),
                 ]
    end_date = datetime.today()
    start_date = end_date - timedelta(days=90)
    start_date = start_date

    df = generate_portfolio_report(portfolio, start_date, end_date)
    print(df)
