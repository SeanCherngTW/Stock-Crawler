#! /usr/bin/env python
#encoding: utf-8

# http://127.0.0.1:2330/overview?stock_id=2330

from config import logger
from stock_crawler import StockCrawler
from flask import Flask, request

app = Flask(__name__)
crawler = StockCrawler()


@app.route('/overview')
def get_stock_info():
    stock_id = request.args.get('stock_id')
    res = crawler.get_stock_info(stock_id, check_redis=True)
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2330, threaded=True)
