import os
from datetime import datetime, timedelta
from typing import Tuple, List
import jinja2
import argparse
import logging
import analytics
import settings
from emails import EmailSender
from generate_graph import dataframe_to_image

logger = logging.getLogger(__name__)

BUY_VALUE = 0.05  # 5% of lower bound or lower
SELL_VALUE = 0.05  # 5% below upper bound or higher


def get_order_for_vals(value: float, upper: float, lower: float) -> str:
    order = 'Hold'
    if value <= lower + BUY_VALUE * (upper - lower):
        order = 'Buy'
    if value >= upper - SELL_VALUE * (upper - lower):
        order = 'Sell'
    return order


def generate_report_html(start_date, end_date, portfolio, **kwargs):
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    html_template = template_env.get_template('templates/stocks_report.html')
    html = html_template.render(
        portfolio=portfolio,
        start_date=start_date,
        end_date=end_date,
    )
    return html


def send_report(content: str, to: Tuple[str, str], attachments: List[str],
                **kwargs):
    """

    :param to   Tuple of (receiver name, receiver email)
    :return:
    """
    subject = kwargs.get('subject', settings.REPORT_SUBJECT)
    from_address = kwargs.get('from', settings.REPORT_SENDER)
    email_sender = EmailSender(settings.SMTP_SERVER,
                               settings.SMTP_SERVER_PORT,
                               settings.SMTP_SERVER_USER,
                               settings.SMTP_SERVER_PASSWORD)
    email_sender.send_email(from_address,
                            to,
                            subject,
                            content,
                            attachments=attachments)


def generate_stock_report(stocks: List[str], **kwargs):
    portfolio = []
    attachments = []
    end_date = kwargs.get('end_date', datetime.today().strftime('%Y-%m-%d'))
    start_date = datetime.today() - timedelta(days=90)
    start_date = start_date.strftime('%Y-%m-%d')
    start_date = kwargs.get('start_date', start_date)
    should_send_report = False
    for stock in stocks:
        df = analytics.get_data({stock}, start_date, end_date)
        df.dropna(inplace=True)
        rolling_bands_df = analytics.rolling_bands(df, column_name=stock)
        order = get_order_for_vals(rolling_bands_df.tail(1)[stock][0],
                                   rolling_bands_df.tail(1)['Upper'][0],
                                   rolling_bands_df.tail(1)['Lower'][0])
        should_send_report = should_send_report or (order != 'Hold')
        stock_title = f'{stock} report {start_date} - {end_date}'
        dataframe_to_image(rolling_bands_df, f'graph-{stock}.png',
                           graph_title=stock_title,
                           colors={stock: 'blue', 'Lower': 'red', 'Upper': 'red'})
        portfolio.append({
            'title': stock_title,
            'order': order,
            'order_color': 'blue',
            'attachment_number': len(attachments),
        })
        attachments.append(f'graph-{stock}.png')
    html = generate_report_html(portfolio=portfolio,
                                start_date=start_date,
                                end_date=end_date)
    if should_send_report:
        send_report(html, settings.REPORT_RECIPIENT, subject='Stocks tracking report', attachments=attachments)
    for item in attachments:
        os.remove(item)


def parse_args():
    parser = argparse.ArgumentParser(description='Stocks tracking report')
    parser.add_argument('-s', '--stocks', dest='stocks', nargs='+',
                        required=True,
                        help='Stocks to track')
    res = parser.parse_args()
    logger.debug(f'args {res}')
    return res


if __name__ == '__main__':
    args = parse_args()
    stocks = [i.upper() for i in args.stocks]
    generate_stock_report(stocks)
