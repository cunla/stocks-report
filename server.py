import json
import os
import time
from datetime import datetime, timedelta
from flask import Flask, request, abort
from report_gen import generate_portfolio_report_csv
import pandas_datareader as pdr

DATE_FORMAT = '%Y-%m-%d'

app = Flask(__name__,
            static_url_path='',
            static_folder='web')


@app.route('/api/portfolio-report', methods=['POST'])
def generate_portfolio():
    req_data = request.get_json()
    portfolio = [(item['percentage'], item['symbol'].upper()) for item in req_data['portfolio']]
    symbols = [item[1] for item in portfolio]
    if len(set(symbols)) != len(symbols):
        abort(400, 'Portfolio has same symbol multiple times')
    portfolio_sum = sum(item[0] for item in portfolio)
    if portfolio_sum != 1.0:
        abort(400, 'Portfolio percentage do not sum to 100%')
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


@app.route('/api/symbols', methods=['GET'])
def get_all_symbols():
    PATH = 'web/symbols.json'
    last_good_date = datetime.now() - timedelta(days=1)
    if not os.path.exists(PATH) \
            or datetime.fromtimestamp(os.path.getmtime(PATH)) < last_good_date:
        df = pdr.get_nasdaq_symbols()
        df = df['Security Name']
        df.to_json(path_or_buf=PATH)
    all_symbols = json.load(open(PATH, 'r'))
    query = request.args.get('q')
    if query is None or len(query) < 2:
        abort(404, 'At least 3 letters query required')
    query = query.lower()
    res = {k: all_symbols[k]
           for k in all_symbols
           if query in k.lower() or query in all_symbols[k].lower()}
    return res


if __name__ == '__main__':
    app.run(debug=True)
