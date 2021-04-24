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



## 获取在金叉点位后的平均收益
def get_average_earn_after_gold_point(earn_after_gold_points):
    sum = reduce(lambda x, y: x+y, earn_after_gold_points) 
    return round(sum*100/len(earn_after_gold_points), 2)


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


def find_ma(hist):    
    if len(hist) <1:
        return False
    closed_values = []
    for row in hist.iterrows():
        closed_values.append(row[1].get('Close'))
    ma_diff_arr = get_ma_diff_arr(closed_values)
    return not any(ma_diff_arr[0:2]) and all(ma_diff_arr[-2:])


def find_today_ma(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="25d")
    except Exception as ex:
        time.sleep(5)
        return find_today_ma(ticker)
    else:
       return find_ma(hist)


# 获取金叉点后的五日收益，十日收益
def get_diff_of_period(period_hist):
    if len(period_hist) <1:
        return 0
    first_closed_value = period_hist.iloc[0][3]
    last_closed_value = period_hist.iloc[-1][3]
    return round( (last_closed_value-first_closed_value)/first_closed_value, 4)


# 找到历史上的金叉点位
def find_history_ma(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
    except Exception as ex:
        time.sleep(5)
        return find_history_ma(ticker)
    else:
        day_five_earn_arr = []
        day_ten_earn_arr = []
        for  i in range(0, len(hist)-30):
            current_hist = hist[i: 25+i]
            is_find_ma =  find_ma(current_hist)
            if is_find_ma:
                day_five_earn = get_diff_of_period(hist[25+i:30+i])
                day_ten_earn = get_diff_of_period(hist[25+i:35+i])
                day_five_earn_arr.append(day_five_earn)
                day_ten_earn_arr.append(day_ten_earn)
        average_day_five_earn=0
        average_day_ten_earn=0
        if len(day_five_earn_arr) > 0:
            average_day_five_earn = get_average_earn_after_gold_point(day_five_earn_arr)
        if len(day_ten_earn_arr) > 0:
            average_day_ten_earn = get_average_earn_after_gold_point(day_ten_earn_arr)
        print(day_five_earn_arr, day_ten_earn_arr, average_day_five_earn, average_day_ten_earn)
        return True
        # return find_ma(hist)


def find_all_ma():
    stock_list = pd.read_csv('../tipranks/all_index.csv')
    stocks = stock_list['Ticker']
    filtered_stocks = []
    for ticker in stocks:        
        if find_today_ma(ticker):
            print(filtered_stocks)
            filtered_stocks.append(ticker)
    return filtered_stocks


def find_history_gold_regression():
    # all_ma_ticker = find_all_ma()
    all_ma_ticker = ['CHTR', 'FOXA', 'FOX', 'MRK', 'LLY', 'CMI', 'PPL', 'VAR', 'BF.B', 'DVA']
    for ticker in all_ma_ticker:
        find_history_ma(ticker)


find_history_gold_regression()

# period="1mo"

## 拿到一个最近25天的单日跌幅排行
## 持有5天或者盈利5%，止损5%
## 做一个回归，上面几次交叉之后5个交易日的收益情况。
## 动态地去获取最新地股票列表


#  2021-04-08 ['GOOG', 'GOOGL', 'ISRG', 'ATVI', 'ADSK', 'DXCM', 'FOX', 'BRK.B', 'MDT', 'NEE', 'ORCL', 'NOW', 'SYK', 'ETN', 'ECL', 'AON', 'EW', 'EOG', 'WMB', 'WY', 'CBRE', 'VFC', 'ZBRA', 'OKE', 'IP', 'DRI', 'HES', 'AMCR', 'NVR', 'STX', 'WRK', 'BF.B', 'PWR', 'CMA', 'COG', 'X9USDMORS']
#   ['CHTR', 'FOXA', 'FOX', 'BRK.B', 'MRK', 'LLY', 'CMI', 'PPL', 'VAR', 'BF.B', 'DVA', 'X9USDMORS']


# 如果盈利概率0.75,亏损概率0.25，盈利平均利润率3%,亏损5%必须离场。
# 在复利的情况下计算总的利润。

# win_oppo = 0.75
# loss_oppo = 0.25
# win_pent = 0.03
# loss_pent = 0.05

# np.random.seed(0)
# p = np.array([0.1, 0.0, 0.7, 0.2])
# index = np.random.choice([0, 1, 2, 3], p = p.ravel())

# np 指定概率


## self watch list


## 10天， 两周，150$ 左右 25* 6 = 150



def perfect_result():
    result =1500
    for i in range(1,26):
        result = result * 1.06 - 6 - round(result * 0.05 /36, 2)
    print(result)
    # 5907


# 最后生成的数据，ticker , company name , current price, 平均5日后涨幅，平均十日后涨幅，上一次五日后涨幅，上一次十日后涨幅。上一次金叉时间，上一次金叉位置

