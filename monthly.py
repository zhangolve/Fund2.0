#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# import flask
import requests
import json
from mail_sender import MailSender
from getInfo import getGegu, getJijin
from readTxt import GetData
from plot import write_plot
import datetime
import os
from functools import reduce


now = datetime.datetime.now()


my_sender = '1262010981@qq.com'
my_pass = 'nrrejsviolzpjchd'
receiver_addr = ['zhangolve@gmail.com']
sender_name = 'FundCalculator'
subject = 'MonthlyFundReport ' + now.strftime("%Y-%m-%d %H:%M:%S")

def get_zhangfu(a, b): 
    diff = round(a-b, 4)
    zhangfu = round(round(diff/b, 4) *100, 2)
    return zhangfu

def get_zhangfu_list(LSJZList):
    day_values = list(map(lambda x: float(x.get('DWJZ')), LSJZList))
    last_day_value = day_values[-1]
    zhangfu_list = list(map(lambda x: get_zhangfu(x, last_day_value), day_values))
    return zhangfu_list


def get_ma(LSJZList):
    jz_list = list(map(lambda x: float(x.get('DWJZ')), LSJZList))
    sum = reduce(lambda x, y: x+y, jz_list) 
    ma = round(sum/len(LSJZList), 2)
    return ma


def today_ma(LSJZList_list):
    ma_10 = get_ma(LSJZList_list[0:10])
    ma_20 = get_ma(LSJZList_list)
    diff = round(ma_10-ma_20,2)
    diff_percent = round(diff/ma_20, 2)
    if diff >0:
        info = '可买'
    else:
        info = '可卖'
    info = info + '净值差' + 'diff' + '比例差' +  str(diff_percent)
    today_ma_info = '今日' 'ma10:' + str(ma_10) + '  ma20:' + str(ma_20) + info  
    return today_ma_info


def get_single_monthly_report(jjcode, name): 
    headers = {'Referer': 'http://fundf10.eastmoney.com/'}
    jjcode_value = jjcode.strip()
    monthly_data_json = requests.get('http://api.fund.eastmoney.com/f10/lsjz?fundCode='+ jjcode_value + '&pageIndex=1&pageSize=20', headers=headers)
    status = monthly_data_json.status_code
    if status != 200:
        return False        
    monthly_data = json.loads(monthly_data_json.text)
    data = monthly_data.get('Data')
    LSJZList = data.get('LSJZList')
    first_day = LSJZList[0] # DWJZ, FSRQ
    last_day = LSJZList[-1]
    first_day_day = first_day.get('FSRQ')
    first_day_value= float(first_day.get('DWJZ'))
    last_day_day = last_day.get('FSRQ')
    last_day_value = float(last_day.get('DWJZ'))
    pre_day = LSJZList[1]
    pre_day_day = pre_day.get('FSRQ')
    pre_day_value = float(pre_day.get('DWJZ'))
    pre_zhangfu = get_zhangfu(first_day_value, pre_day_value)
    monthly_zhangfu = get_zhangfu(first_day_value, last_day_value) 
    pre_diff_info = '今日涨幅:' + str(pre_zhangfu);
    LSJZList_list = [*LSJZList]
    today_ma_info = today_ma(LSJZList_list)
    content = name + jjcode_value + '\n' + first_day_day + ':'+ str(first_day_value) + '\n' + last_day_day + ':'+ str(last_day_value) + '\n' + pre_diff_info + '\n' +  '20个交易日共收益' + str(monthly_zhangfu) + '\n' + today_ma_info
    return content, get_zhangfu_list(LSJZList)
   

def get_monthly_report():
    d = GetData()
    jjc = d.getJjCode()
    content = []
    jj_zhangfu_list = []
    for i in jjc:
        jj, jj_jin = getJijin(i.strip())
        name = ''
        jjcode = i
        if jj != False:
            name, guzhi, gutime = jj['name'], jj['gszzl'] + '%', jj['gztime']
        jj_content, zhangfu_list = get_single_monthly_report(jjcode,name)
        content.append(jj_content)
        zhangfu_list.reverse()
        jj_zhangfu_list.append(dict(label=name if name else jjcode, data=zhangfu_list))
    content = '\n\n\n'.join(content)
    attachment = './result.png'
    # print(content)
    jj_zhangfu_list.reverse()
    write_plot(jj_zhangfu_list, attachment)
    mailsender=MailSender(my_sender, my_pass, sender_name, receiver_addr, subject, content, attachment)
    mailsender.send_it()
    if os.path.exists(attachment):
        os.remove(attachment)   

get_monthly_report()

