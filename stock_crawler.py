import time
import json
import requests
import redis_manager
from config import logger
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
from selenium import webdriver


class StockCrawler:
    def __init__(self):
        self.driver = webdriver.PhantomJS(executable_path='./phantomjs-2.1.1-macosx/bin/phantomjs')
        self.redis_manager = redis_manager.RedisManager('127.0.0.1', '6379')

    def get_stock_info(self, stock_id, check_redis=True):
        now_date = datetime.now()

        if now_date.hour <= 13:
            last_market_closed = (now_date - timedelta(days=1)).replace(hour=14, minute=0, second=0)
        else:
            last_market_closed = now_date.replace(hour=14, minute=0, second=0)

        if check_redis and self.redis_manager.exists(stock_id):
            res = eval(self.redis_manager.get(stock_id))
            update_date = datetime.strptime(res['update_date'], "%Y/%m/%d %H:%M")
            if update_date > last_market_closed:
                logger.info('Get data from Redis')
                return res

        logger.info('Get data from Crawler')
        url = 'https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID={}'.format(stock_id)
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        res = {}
        res['id'] = stock_id
        res['name'] = self.get_name(soup, stock_id)
        res['beta'] = self.get_beta(soup, stock_id)
        res['update_date'] = datetime.now().strftime("%Y/%m/%d %H:%M")

        self.redis_manager.set(stock_id, res, to_json=True)

        return res

    def get_name(self, soup, stock_id):
        raw_id_name = soup.find(
            name="a",
            class_="link_blue",
            href='StockDetail.asp?STOCK_ID={}'.format(stock_id),
        ).text

        splitter = raw_id_name.find('\xa0')
        parsed_id, name = raw_id_name[:splitter], raw_id_name[splitter + 1:]
        assert parsed_id == stock_id, 'Parsed stock_id not match: got {} v.s. {}'.format(parsed_id, stock_id)
        return name

    def get_beta(self, soup, stock_id):
        raw_beta = soup.find(
            name="table",
            class_='solid_1_padding_4_2_tbl',
            style='font-size:11pt;line-height:20px;',
        ).find_all('td')

        header = raw_beta[0]
        assert header.find('nobr').text == '風險係數', 'soup parser error, 風險指數 not found in {}'.format(header)

        num_interval = len(raw_beta) // 2
        intervals = raw_beta[1:num_interval + 1]
        values = raw_beta[num_interval + 1:]

        res = {}
        interval_to_numeric_map = {
            '5日': '5', '10日': '10',
            '一個月': '20', '三個月': '60',
            '半年': '120', '一年': '240', '三年': '720',
            '五年': '1200', '十年': '2400', '二十年': '4800',
        }
        for interval, value in zip(intervals, values):
            res[interval_to_numeric_map[interval.find('nobr').text]] = value.text

        return res
