import json
import os
from datetime import datetime, timedelta

import pandas_datareader as pdr
from flask import Flask, request, abort, Response

from db import Portfolio
from report_gen import generate_portfolio_report_csv

DATE_FORMAT = '%Y-%m-%d'

app = Flask(__name__,
            static_url_path='',
            static_folder='./web/www')


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/stock/<path:path>')
def static_file(path):
    return app.send_static_file('index.html')


def get_portfolio(portfolio_req):
    if isinstance(portfolio_req, dict):
        return [(portfolio_req[k], k.upper()) for k in portfolio_req]
    if isinstance(portfolio_req, list):
        return [(item['percentage'], item['symbol'].upper()) for item in portfolio_req]
    return None


@app.route('/api/portfolio-report', methods=['POST'])
def portfolio_report():
    req_data = request.get_json()
    portfolio = get_portfolio(req_data['portfolio'])
    symbols = [item[1] for item in portfolio]
    if len(set(symbols)) != len(symbols):
        abort(400, 'Portfolio has same symbol multiple times')
    if any(item[0] != int(item[0]) for item in portfolio) and sum(item[0] for item in portfolio) != 1.0:
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


def get_symbols(query: str) -> dict[str, str]:
    PATH = './web/symbols.json'
    last_good_date = datetime.now() - timedelta(days=1)
    if not os.path.exists(PATH) \
            or datetime.fromtimestamp(os.path.getmtime(PATH)) < last_good_date:
        df = pdr.get_nasdaq_symbols()
        df = df['Security Name']
        df.to_json(path_or_buf=PATH)
    all_symbols = json.load(open(PATH, 'r'))
    query = query.lower()
    res = {k: all_symbols[k]
           for k in all_symbols
           if query in k.lower() or query in all_symbols[k].lower()}
    return res


@app.route('/api/symbols', methods=['GET'])
def get_all_symbols():
    query = request.args.get('q', default='')
    if query is None or len(query) < 2:
        abort(404, 'At least 2 letters query required')
    return get_symbols(query)


@app.route('/api/symbols-list', methods=['GET'])
def get_symbols_list():
    query = request.args.get('q', default='')
    if query is None or len(query) < 2:
        abort(404, 'At least 2 letters query required')
    res_dict = get_symbols(query)
    res_list = list({'symbol': k, 'name': res_dict[k]} for k in res_dict)
    return Response(json.dumps(res_list), mimetype='application/json')


@app.route('/api/portfolios', methods=['POST'])
def portfolio_create():
    req_data = request.get_json()
    portfolio = Portfolio.create(req_data['name'], req_data['mix'])
    return portfolio.to_json()


@app.route('/api/portfolios/<int:p_id>', methods=['GET'])
def portfolio_detail(p_id: int):
    portfolio = Portfolio.get(p_id)
    if portfolio is None:
        abort(404, 'Portfolio not found')
    return portfolio.to_json()


@app.route('/api/portfolios', methods=['GET'])
def portfolio_list():
    query = request.args.get('q', default='')
    portfolios = Portfolio.list(query)
    res = {'results': [p.to_json() for p in portfolios]}
    return res


if __name__ == '__main__':
    app.run(debug=True)
