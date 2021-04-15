#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
import json
from mail_sender import MailSender
from getInfo import getGegu, getJijin, today_ma, today_ma_5
from readTxt import GetETFData
from plot import write_plot
import datetime
import os
import functools


now = datetime.datetime.now()


my_sender = '1262010981@qq.com'
my_pass = 'nrrejsviolzpjchd'
receiver_addr = ['zhangolve@gmail.com']
sender_name = 'ETF report'
subject = 'DailyETFReport ' + now.strftime("%Y-%m-%d %H:%M:%S")




def get_single_etf_report(jjcode, name): 
    headers = {'Referer': 'http://fundf10.eastmoney.com/'}
    jjcode_value = jjcode.strip()
    monthly_data_json = requests.get('http://api.fund.eastmoney.com/f10/lsjz?fundCode='+ jjcode_value + '&pageIndex=1&pageSize=25', headers=headers)
    status = monthly_data_json.status_code
    if status != 200:
        return False        
    monthly_data = json.loads(monthly_data_json.text)
    data = monthly_data.get('Data')
    ALL_LSJZList = data.get('LSJZList')
    today_ma_info = today_ma(ALL_LSJZList)
    today_ma_5_info = today_ma_5(ALL_LSJZList)
    content = name + jjcode_value + '\n'  + today_ma_info + '\n' + today_ma_5_info
    return content
   

def cmp(a, b):
    if '可买' in a and '可买' not in b:
        return -1
    if '可卖' in a and '可卖' not in b:
        return 1
    return 0


def get_buy_and_sell_etf():
    d = GetETFData()
    jjc = d.getJjCode()
    content = []
    for i in jjc:
        jjcode = i.strip().split(',')[0]
        is_hold = len(i.strip().split(',')) > 1 
        jj, jj_jin = getJijin(i.strip())
        name = ''
        if jj != False:
            name = jj['name']
        jj_content = get_single_etf_report(jjcode,name)
        if is_hold and ('可买' in jj_content or '可卖' in  jj_content):
            content.append(jj_content)
        else:
            if '可买' in jj_content:
                content.append(jj_content)
    sorted(content, key=functools.cmp_to_key(cmp))
    content = '\n\n\n'.join(content)
    mailsender=MailSender(my_sender, my_pass, sender_name, receiver_addr, subject, content,None)
    mailsender.send_it()


get_buy_and_sell_etf()