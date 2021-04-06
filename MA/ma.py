#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import yfinance as yf

QQQ = yf.Ticker("QQQ")

hist = QQQ.history(period="max")
for row in hist.iterrows():
    print(type(row[1]))
    # <class 'pandas.core.series.Series'
    print(row[1].get('Close'))
    # 20， 10