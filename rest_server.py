from config import logger
from stock_crawler import StockCrawler
from flask import Flask, request, jsonify, Response, render_template

app = Flask(__name__)
crawler = StockCrawler()


@app.route('/overview')
def get_stock_info():
    stock_id = request.args.get('stock_id')
    res = crawler.get_stock_info(stock_id, check_redis=True)
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2330, threaded=True)
