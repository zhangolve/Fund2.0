#!/usr/bin/env python
# -*- coding: utf-8 -*- 

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
from mail_sender import MailSender


my_sender = '1262010981@qq.com'
my_pass = 'nrrejsviolzpjchd'
receiver_addr = ['zhangolve@gmail.com']
sender_name = 'FundCalculator'

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
stock_list = pd.read_csv('all_index.csv')

stocks = stock_list['Ticker']

now = datetime.datetime.now()
result_csv = 'picked_stocks-' + now.strftime("%Y-%m-%d") + '.csv'


def init_result_csv():
    if not os.path.exists(result_csv):
        df = pd.DataFrame()
        df['stock_ticker'] = []
        df['stock_name'] = []
        df['curr_price'] = []
        df['pred_low'] = []
        df['pred_avg'] = []
        df['pred_high'] = []
        df['# of Analyst'] = []
        df['% low/curr'] = []
        df['% avg/curr'] = []
        df['% high/curr'] = []
        df.to_csv(result_csv, index=None, mode='w')


def get_now_timestamp():
    now = datetime.datetime.now() # 获取当前datetime
    timestamp = str(int(now.timestamp() * 1000 ))
    return timestamp


def get_one_stock_data(ticker):
    timestamp = get_now_timestamp()
    url = 'https://www.tipranks.com/api/stocks/getData/?name='+ticker+'&benchmark=1&period=3&break='+timestamp
    stock_data_json = requests.get(url, timeout=(5, 27))
    status = stock_data_json.status_code
    if status != 200:
        logger.error(stock_data_json)
        logger.error(ticker)
        if status == 404:
            return False
        else:
            raise Exception('stock data request failed')
    stock_data_json = json.loads(stock_data_json.text) 
    return stock_data_json


def get_curr_price(ticker):
    timestamp = get_now_timestamp()
    url = 'https://market.tipranks.com/api/details/getstockdetailsasync/?break='+timestamp + '&id='+ticker
    ticker_detail_json = requests.get(url, timeout=(5, 27))
    status = ticker_detail_json.status_code
    if status != 200:
        logger.error(ticker_detail_json)
        logger.error(ticker)
        # Todo: 404 handle
        if status == 404:
            return False
        else:
            raise Exception('request failed')
    ticker_detail = json.loads(ticker_detail_json.text)
    curr_price = ticker_detail[0].get('price')
    return curr_price


def get_target_price(ticker):
    stock_data = get_one_stock_data(ticker)
    if not stock_data:
        return False
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
    init_result_csv()
    if os.path.exists(result_csv):
        existing_stock_list = pd.read_csv(result_csv)
        existing_ticker_series = existing_stock_list['stock_ticker']
        for t in existing_ticker_series:
            existing_ticker.append(t)
    for ticker in stocks:
        if ticker and ticker not in existing_ticker:
            logger.info('start fech data:')
            logger.info(ticker)
            stock_ticker = []
            stock_name = []
            curr_price = []
            pred_low = []
            pred_avg = []
            pred_high = []
            num_analyst = []
            s_curr_price = get_curr_price(ticker)
            if not s_curr_price:
                continue
            data = get_target_price(ticker)
            if not data:
                continue
            [companyName, high, low, priceTarget, s_num_analyst] = data
            if s_num_analyst and priceTarget and low and high:
                curr_price.append(s_curr_price)
                pred_low.append(low)
                pred_high.append(high)
                num_analyst.append(s_num_analyst)
                pred_avg.append(priceTarget)
                stock_ticker.append(ticker)
                stock_name.append(companyName)
                info = companyName + ' created'
                logger.info(info)
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
                df.to_csv(result_csv, index=None, mode='a+', header=False)
       
    if os.path.exists(result_csv):
        attachment = result_csv
        content = 'ripranks'
        now = datetime.datetime.now()
        subject = 'tipranks result ' + now.strftime("%Y-%m-%d %H:%M:%S")
        mailsender = MailSender(my_sender, my_pass, sender_name, receiver_addr, subject, content, attachment)
        mailsender.send_it()


exec_count = 0
def exec():
    global exec_count
    exec_count += exec_count
    if exec_count < 100:  
        try: 
            init()
        except Exception as ex:
            print(ex)
            logger.error(ex)
            time.sleep(5)
            exec()
    else: 
        now = datetime.datetime.now()
        subject = 'tipranks exeception ' + now.strftime("%Y-%m-%d %H:%M:%S")
        attachment = './error.log'
        content="got exeception"
        mailsender = MailSender(my_sender, my_pass, sender_name, receiver_addr, subject, content, attachment)
        mailsender.send_it()

exec()