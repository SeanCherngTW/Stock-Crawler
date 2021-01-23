from stock_crawler import StockCrawler

if __name__ == '__main__':
    crawler = StockCrawler()
    print(crawler.get_stock_info('2330', check_redis=False))
    print(crawler.get_stock_info('2330', check_redis=True))
    print(crawler.get_stock_info('2754', check_redis=False))
    print(crawler.get_stock_info('2754', check_redis=True))
