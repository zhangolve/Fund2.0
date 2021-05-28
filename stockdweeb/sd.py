import bs4 as bs
import os
import requests
import pandas as pd
import json
import datetime
import yfinance as yf
import time
from mail_sender import MailSender


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'cookie': 'wordpress_logged_in_eee975233d79b33c61574e047140d50d=zhangolve%40gmail.com%7C1623107386%7CIS13Fkz37ZsTgutDhk4jm1FebUi0ogUJQvAiIwXBZdi%7C80529f10b4655e9911af124e228e05e8a87eaaf6e9a3c6be36dc7a44c25471a4'
}

data_path = 'data.txt'

failed_times = 0
max_failed_times= 3


## mail info
my_sender = '1262010981@qq.com'
my_pass = 'nrrejsviolzpjchd'
receiver_addr = ['zhangolve@gmail.com']
sender_name = 'StockDweebs'
now = datetime.datetime.now()
subject = 'stock dweeb pickup ' + now.strftime("%Y-%m-%d %H:%M:%S")


def save_json():   
    try:
        resp = requests.get('https://stockdweebs.com/pick_categories/weekly-picks/', headers=headers)           
        soup = bs.BeautifulSoup(resp.text, 'html.parser')
        table = soup.find('div', {'class': 'archive-feed-pick'})
        symbols = []
        for row in table.findAll('article'):
            symbol = row.get('data-stock-symbol')
            buy_zones_parent = row.findAll('span', {'class','data-value'})[-2]
            buy_zones =  buy_zones_parent.findAll('span', {'class','buy-zone'})
            entry = buy_zones[0].text[1:]
            stop = buy_zones[-1].text[1:]
            single_symbol = dict(entry=entry, symbol=symbol, stop=stop)
            symbols.append(single_symbol)
        
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        symbols_json = dict(symbols=symbols, time=time)
        fo = open(data_path, "w")
        json.dump(symbols_json, fo)
        fo.close()
    except Exception as ex:
        global failed_times
        failed_times +=1
        if failed_times > max_failed_times:
            content = "EXCEPTION FORMAT PRINT:\n{}".format(ex)
            mailsender=MailSender(my_sender, my_pass, sender_name, receiver_addr, subject, content, None)
            mailsender.send_it()
        else:
            save_json()


def get_single_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        current_price = stock.info['regularMarketPrice']
        return float(current_price)
    except Exception as ex:
        time.sleep(5)
        return get_single_stock_price(ticker)


def load_json():
    if datetime.datetime.today().weekday() ==1:
        # 周二刷新
        save_json()
    if not os.path.exists(data_path):
        save_json()
    with open(data_path) as json_file:
        data = json.load(json_file)
        time = data.get('time')
        now = datetime.datetime.now()
        datetime_format_time = datetime.datetime.fromisoformat(time)
        if now-datetime_format_time > datetime.timedelta(days=7):
            save_json()
            return load_json()
        else:
            symbols = data.get('symbols')
            return symbols


def init():
    symbols = load_json()
    content = ''
    for single_symbol in symbols:
        symbol = single_symbol.get('symbol')
        entry = float(single_symbol.get('entry'))
        stop = float(single_symbol.get('stop'))
        current_price = get_single_stock_price(symbol)
        if current_price < entry and current_price > stop:
            single_content = 'symbol:' + symbol + '\n entry price: ' + str(entry) +  '\n current price: ' + str(current_price) + '\n stop price:' + str(stop) + '\n' 
            content += single_content
    if len(content) > 0 :
        mailsender=MailSender(my_sender, my_pass, sender_name, receiver_addr, subject, content, None)
        mailsender.send_it()


init()