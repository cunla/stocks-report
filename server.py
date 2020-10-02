from datetime import datetime, timedelta

from flask import Flask, request
from report_gen import generate_portfolio_report_csv

app = Flask(__name__)

DATE_FORMAT = '%Y-%m-%d'


@app.route('/portfolio-report', methods=['POST'])
def hello_world():
    req_data = request.get_json()
    portfolio = [(item['percentage'], item['symbol']) for item in req_data['portfolio']]
    end_date = datetime.today().date()
    if 'endDate' in req_data:
        end_date = datetime.strptime(req_data['endDate'], DATE_FORMAT).date()
    start_date = end_date - timedelta(days=90)
    if 'startDate' in req_data:
        start_date = datetime.strptime(req_data['startDate'], DATE_FORMAT).date()

    results = generate_portfolio_report_csv(portfolio, start_date, end_date, columns=['portfolio', 'Upper', 'Lower'])
    return {
        'startDate': start_date.strftime(DATE_FORMAT),
        'endDate': end_date.strftime(DATE_FORMAT),
        'csv': results
    }


if __name__ == '__main__':
    app.run(debug=True)
