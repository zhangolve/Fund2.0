#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import yfinance as yf
import pandas as pd
from functools import reduce
import time


# 回归


def get_ma(closed_values):
    sum = reduce(lambda x, y: x+y, closed_values) 
    ma = round(sum/len(closed_values), 2)
    return ma


def get_ma_diff_arr(closed_values):
    diff_bools = []
    index = 0
    diff_range = len(closed_values[19:])
    for i in range(0, diff_range):
        ma_20 = get_ma(closed_values[i: 20+i])
        ma_10 = get_ma(closed_values[10+i: 20+i])
        diff_bools.append(ma_10-ma_20>0)
    return diff_bools


def regression(ticker):
    stock = yf.Ticker(ticker)

    hist = stock.history(period="max")
    for row in hist.iterrows():
        print(type(row[1]))
        # <class 'pandas.core.series.Series'
        print(row[1].get('Close'))
        # %
        # ma
        # 20， 10
        #寻找双均线金叉点位
        # 比照ma5，ma10 vs ma10 vs ma20 哪个更合适



def find_ma(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="25d")
    except Exception as ex:
        time.sleep(5)
        return find_ma(ticker)
    else:
        closed_values = []
        for row in hist.iterrows():
            closed_values.append(row[1].get('Close'))
        ma_diff_arr = get_ma_diff_arr(closed_values)
        return not any(ma_diff_arr[0:2]) and all(ma_diff_arr[-2:])


def find_all_ma():
    stock_list = pd.read_csv('../tipranks/all_index.csv')
    stocks = stock_list['Ticker']
    filtered_stocks = []
    for ticker in stocks:        
        if find_ma(ticker):
            print(filtered_stocks)
            filtered_stocks.append(ticker)
    print(filtered_stocks)


find_all_ma()
# period="1mo"

# ['GOOG', 'GOOGL', 'ISRG', 'ATVI', 'ADSK', 'DXCM', 'FOX', 'BRK.B', 'MDT', 'NEE', 'ORCL', 'NOW', 'SYK', 'ETN', 'ECL', 'AON', 'EW', 'EOG', 'WMB', 'WY', 'CBRE', 'VFC', 'ZBRA', 'OKE', 'IP', 'DRI', 'HES', 'AMCR', 'NVR', 'STX', 'WRK', 'BF.B', 'PWR', 'CMA', 'COG', 'X9USDMORS']
# 