#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import yfinance as yf
import pandas as pd
from functools import reduce
import time
import csv

# from ..tipranks  import save_index



# 尝试很多解决方法，包括给evaluation_metrics文件夹下添加__init__.py文件，让python能够识别。可是依旧如此。总结了下，后来觉得自己应该是没有在main.py下运行，但是我又不想在造一个main文件，于是把相对路径导入改为顶级目录下的导入，实现很简单：

# from mmt.evaluation_metrics import accuracy
# 将要导入的方法和需要导入的函数的顶级目录加上就可以了。
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
    # 仅仅刚刚过了金叉点,一个交易日或者两个交易日
    return not any(ma_diff_arr[0:2]) and all(ma_diff_arr[-1:])


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
    # 注意是开盘价，不是前一天的收盘价。
    # - X9USDMORS: No data found, symbol may be delisted
    # Date  Open   High  Low  close   Volume  Dividends  Stock Splits
    first_closed_value = period_hist.iloc[0][1]
    last_closed_value = period_hist.iloc[-1][1]
    return round( (last_closed_value-first_closed_value)/first_closed_value, 4)


# 找到历史上的金叉点位
def find_history_ma(ticker, period):
    current_period  = period or "1y"
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=current_period)
        len(hist)
    except Exception as ex:
        time.sleep(5)
        return find_history_ma(ticker, current_period)
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
        last_day_five_earn_arr = day_five_earn_arr[-1] if len(day_five_earn_arr) >0 else ''
        last_day_ten_earn_arr = day_ten_earn_arr[-1] if len(day_ten_earn_arr) >0 else ''
        return [str(last_day_five_earn_arr), str(last_day_ten_earn_arr), str(average_day_five_earn), str(average_day_ten_earn)]


def find_all_ma():
    stock_list = pd.read_csv('../tipranks/all_index.csv')
    stocks = stock_list['Ticker']
    filtered_stocks = []
    for ticker in stocks:        
        if ticker and find_today_ma(ticker):
            print(filtered_stocks)
            filtered_stocks.append(ticker)
    return filtered_stocks




def write_to_csv(datas):
    with open('filtered_stocks.csv', 'w', newline='',encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar=',', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['ticker','上次交叉后5天收益', '上次交叉后10天收益','1年平均5天收益','1年平均10天收益','3年平均5天收益','3年平均10天收益'])
        for data in datas:
            spamwriter.writerow(data)


def find_history_gold_regression():
    # all_ma_ticker = find_all_ma()
    all_ma_ticker = ['CHTR', 'FOXA', 'FOX', 'MRK', 'LLY', 'STZ', 'CNC', 'PPL', 'CAG', 'LW', 'PRGO', 'COIN']
    datas = []
    for ticker in all_ma_ticker:
        if ticker: 
            history_ma_one_year = find_history_ma(ticker,'1y')
            history_ma_three_year = find_history_ma(ticker,'3y')
            data = [ticker] + history_ma_one_year + history_ma_three_year[-2:]
            datas.append(data)
    write_to_csv(datas)



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

