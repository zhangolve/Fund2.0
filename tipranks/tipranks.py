import time
import pandas as pd
import numpy as np
import requests
import json
import os
import logging
import sys

import logging.handlers
import datetime
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

rf_handler = logging.handlers.TimedRotatingFileHandler('all.log', when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

f_handler = logging.FileHandler('error.log')
f_handler.setLevel(logging.ERROR)
f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

logger.addHandler(rf_handler)
logger.addHandler(f_handler)


#Importing a list of stock tickers
pwd = os.getcwd()
stock_list = pd.read_csv('Russell3000stocks.csv')

stocks = stock_list['Ticker']

stock_ticker = []
stock_name = []
curr_price = []
pred_low = []
pred_avg = []
pred_high = []
num_analyst = []
count = 0

def get_now_timestamp():
    now = datetime.datetime.now() # 获取当前datetime
    timestamp = str(int(now.timestamp() * 1000 ))
    return timestamp

def get_one_stock_data(ticker):
    timestamp = get_now_timestamp()
    url = 'https://www.tipranks.com/api/stocks/getData/?name='+ticker+'&benchmark=1&period=3&break='+timestamp
    stock_data_json = requests.get(url)
    status = stock_data_json.status_code
    if status != 200:
        logger.error('stock data request failed')
    stock_data_json = json.loads(stock_data_json.text) 
    return stock_data_json


def get_curr_price(ticker):
    timestamp = get_now_timestamp()
    url = 'https://market.tipranks.com/api/details/getstockdetailsasync/?break='+timestamp + '&id='+ticker
    ticker_detail_json = requests.get(url)
    status = ticker_detail_json.status_code
    if status != 200:
        logger.error('request failed')
    ticker_detail = json.loads(ticker_detail_json.text)
    curr_price = ticker_detail[0].get('price')
    return curr_price


def get_target_price(ticker):
    stock_data = get_one_stock_data(ticker)
    ptConsensus = stock_data.get('ptConsensus')
    companyName = stock_data.get('companyName')
    [high, low, priceTarget]=[None, None, None]
    if ptConsensus:
        result = ptConsensus[-1]
        high = result.get('high')
        low = result.get('low')
        priceTarget = result.get('priceTarget')
    latestRankedConsensus = stock_data.get('latestRankedConsensus')
    num_analyst = latestRankedConsensus.get('nB') + latestRankedConsensus.get('nH')+ latestRankedConsensus.get('nS')
    return [companyName, high, low, priceTarget, num_analyst]
    # loop all ,get detail


def get_gain(x,y):
    return round(100*(float(x)/float(y)-1),2)


def init():
    existing_ticker = []
    if os.path.exists('Stocks_TipRank_partA_800.csv'):
        existing_stock_list = pd.read_csv('Stocks_TipRank_partA_800.csv')
        existing_ticker_series = existing_stock_list['stock_ticker']
        for t in existing_ticker_series:
            existing_ticker.append(t)
    for ticker in stocks:
        if ticker not in existing_ticker:
            s_curr_price = get_curr_price(ticker)
            data = get_target_price(ticker)
            [companyName, high, low, priceTarget, s_num_analyst] = data
            curr_price.append(s_curr_price)
            pred_low.append(low)
            pred_high.append(high)
            num_analyst.append(s_num_analyst)
            pred_avg.append(priceTarget)
            stock_ticker.append(ticker)
            stock_name.append(companyName)
            info = companyName + 'created'
            logger.info(info)
            time.sleep(3)

    #Temporarily save after every 20 stocks
        # if count%20 == 0:
        #     df = pd.DataFrame()
        #     df['stock_ticker'] = stock_ticker
        #     df['stock_name'] = stock_name
        #     df['curr_price'] = curr_price
        #     df['pred_low'] = pred_low
        #     df['pred_avg'] = pred_avg
        #     df['pred_high'] = pred_high
        #     df['# of Analyst'] = num_analyst
        #     df['% low/curr'] = [get_gain(x,y) for x,y in zip(pred_low,curr_price)]
        #     df['% avg/curr'] = [get_gain(x,y) for x,y in zip(pred_avg,curr_price)]
        #     df['% high/curr'] = [get_gain(x,y) for x,y in zip(pred_high,curr_price)]
        #     df.to_csv('Stocks_TipRank_partA_800.csv', index=None)
        #Last save
        df = pd.DataFrame()
        df['stock_ticker'] = stock_ticker
        df['stock_name'] = stock_name
        df['curr_price'] = curr_price
        df['pred_low'] = pred_low
        df['pred_avg'] = pred_avg
        df['pred_high'] = pred_high
        df['# of Analyst'] = num_analyst
        df['% low/curr'] = [get_gain(x,y) for x,y in zip(pred_low,curr_price)]
        df['% avg/curr'] = [get_gain(x,y) for x,y in zip(pred_avg,curr_price)]
        df['% high/curr'] = [get_gain(x,y) for x,y in zip(pred_high,curr_price)]
        df.to_csv('Stocks_TipRank_partA_800.csv', index=None)


# TODD: get full russel 3000 according to api

try: 
    init()
except Exception as ex:
    print(ex)
    print(ex)
    logger.error(ex)