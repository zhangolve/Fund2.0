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
    content = ['华安创业板50ETF159949\n今日ma10:1.18  ma20:1.16保持[True, True, True, True, True, False]净值差diff比例差0.0172\n今日ma5:1.18  ma10:1.18可卖净值差diff比例差0.0', '海富通上证城投债ETF511220\n今日ma10:97.3  ma20:97.28保持[True, False, False, False, False, False]净值差diff比例差0.0002\n今日ma5:97.35  ma10:97.3保持[True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False]净值差diff比例差0.0005', '汇添富中证主要消费ETF159928\n今日ma10:4.92  ma20:4.85保持[True, True, True, True, True, True]净值差diff比例差0.0144\n今日ma5:4.89  ma10:4.92可卖净值差diff比例差-0.0061', '广发中证全指可选消费ETF159936\n今日ma10:1.97  ma20:1.96保持[True, True, True, False, True, True]净值差diff比例差0.0051\n今日ma5:1.97  ma10:1.97可卖净值差diff比例差0.0', '华夏医药ETF510660\n今日ma10:3.13  ma20:3.05保持[True, True, True, True, True, True]净值差diff比例差0.0262\n今日ma5:3.14  ma10:3.13保持[True, True, True, True, True, True, True, True, True, True, True, False, False, True, False, False]净值差diff比例差0.0032', '易方达沪深300医药ETF512010\n今日ma10:2.91  ma20:2.84保持[True, True, True, True, True, True]净值差diff比例差0.0246\n今日ma5:2.89  ma10:2.91可卖净值差diff比例差-0.0069', '广发中证全指医药卫生ETF159938\n今日ma10:2.05  ma20:2.0保持[True, True, True, True, True, True]净值差diff比例差0.025\n今日ma5:2.05  ma10:2.05可卖净值差diff比例差0.0', '汇添富中证医药卫生ETF159929\n今日ma10:2.32  ma20:2.27保持[True, True, True, True, True, True]净值差diff比例差0.022\n今日ma5:2.3  ma10:2.32可卖净值差diff比例差-0.0086', '广发中证全指信息技术ETF159939\n今日ma10:1.28  ma20:1.26可买净值差diff比例差0.0159\n今日ma5:1.29  ma10:1.28保持[True, True, True, True, True, True, True, True, False, True, False, False, False, False, False, False]净值差diff比例差0.0078', '501029\n今日ma10:1.18  ma20:1.17可买净值差diff比例差0.0085\n今日ma5:1.18  ma10:1.18可卖净值差diff比例差0.0', '华泰柏瑞上证红利ETF510880\n今日ma10:2.76  ma20:2.74保持[True, True, False, False, False, True]净值差diff比例差0.0073\n今日ma5:2.76  ma10:2.76可卖净值差diff比例差0.0', '万家中证红利指数(LOF)161907\n今日ma10:1.96  ma20:1.96保持[False, False, False, False, False, True]净值差diff比例差0.0\n今日ma5:1.97  ma10:1.96保持[True, True, True, True, True, False, False, False, False, False, False, False, False, True, True, True]净值差diff比例差0.0051', '富国中证1000指数增强161039\n今日ma10:1.72  ma20:1.71保持[True, True, True, True, True, True]净值差diff比例差0.0058\n今日ma5:1.74  ma10:1.72保持[True, True, True, True, True, True, True, False, False, False, False, False, True, True, True, True]净值差diff比例差0.0116', '南方中证1000ETF512100\n今日ma10:0.9  ma20:0.89可买净值差diff比例差0.0112\n今日ma5:0.91  ma10:0.9保持[True, True, True, False, True, True, True, False, False, False, False, False, False, True, True, True]净值差diff比例差0.0111', '南方中证500ETF510500\n今日ma10:6.99  ma20:6.94保持[True, True, True, True, True, True]净值差diff比例差0.0072\n今日ma5:7.01  ma10:6.99保持[True, True, True, True, True, True, True, True, False, False, False, False, True, True, True, True]净值差diff比例差0.0029', '华泰柏瑞沪深300ETF510300\n今日ma10:5.08  ma20:5.06可买净值差diff比例差0.004\n今日ma5:5.07  ma10:5.08可卖净值差diff比例差-0.002', '易方达深证100ETF159901\n今日ma10:6.78  ma20:7.08保持[False, False, True, True, True, False]净值差diff比例差-0.0424\n今日ma5:6.01  ma10:6.78可卖净值差diff比例差-0.1136', '易方达创业板ETF159915\n今日ma10:2.69  ma20:2.64保持[True, True, True, True, True, True]净值差diff比例差0.0189\n今日ma5:2.7  ma10:2.69保持[True, True, True, True, True, True, True, True, False, False, False, False, False, False, True, False]净值差diff比例差0.0037', '广发中证环保ETF512580\n今日ma10:1.18  ma20:1.16保持[True, True, False, False, True, False]净值差diff比例差0.0172\n今日ma5:1.17  ma10:1.18可卖净值差diff比例差-0.0085', '国泰中证全指证券公司ETF512880\n今日ma10:1.04  ma20:1.04保持[False, False, False, False, False, False]净值差diff比例差0.0\n今日ma5:1.04  ma10:1.04保持[False, False, False, False, False, False, False, False, True, True, False, False, False, False, False, False]净值差diff比例差0.0', '易方达证券公司(LOF)502010\n今日ma10:1.17  ma20:1.18保持[False, False, False, False, False, True]净值差diff比例差-0.0085\n今日ma5:1.17  ma10:1.17保持[False, False, False, False, False, False, False, False, True, True, True, True, False, False, False, False]净值差diff比例差0.0', '513500\n今日ma10:2.5  ma20:2.46保持[True, True, True, True, True, True]净值差diff比例差0.0163\n今日ma5:2.53  ma10:2.5保持[True, True, True, True, True, True, True, True, False, False, False, False, False, True, True, True]净值差diff比例差0.012', '513030\n今日ma10:1.21  ma20:1.2保持[True, True, True, True, False, True]净值差diff比例差0.0083\n今日ma5:1.23  ma10:1.21保持[True, True, True, True, True, True, False, False, False, False, False, True, True, False, False, True]净值差diff比例差0.0165', '华夏上证50AH优选指数A501050\n今日ma10:1.65  ma20:1.64可买净值差diff比例差0.0061\n今日ma5:1.64  ma10:1.65可卖净值差diff比例差-0.0061', '513100\n今日ma10:4.49  ma20:4.41保持[True, True, True, True, True, True]净值差diff比例差0.0181\n今日ma5:4.58  ma10:4.49保持[True, True, True, True, True, True, True, False, False, False, False, False, False, True, True, True]净值差diff比例差0.02', '159941\n今日ma10:2.71  ma20:2.66保持[True, True, True, True, True, True]净值差diff比例差0.0188\n今日ma5:2.77  ma10:2.71保持[True, True, True, True, True, True, True, False, False, False, False, False, False, True, True, True]净值差diff比例差0.0221', '国泰黄金ETF518800\n今日ma10:3.55  ma20:3.55保持[False, True, False, False, True, True]净值差diff比例差0.0\n今日ma5:3.58  ma10:3.55保持[True, True, True, False, False, False, False, False, False, False, True, True, True, True, True, True]净值差diff比例差0.0085', '汇添富中证金融地产ETF159931\n今日ma10:1.79  ma20:1.81保持[False, False, False, False, False, False]净值差diff比例差-0.011\n今日ma5:1.78  ma10:1.79保持[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]净值差diff比例差-0.0056', '国泰上证180金融ETF510230\n今日ma10:1.16  ma20:1.17保持[False, False, False, False, False, False]净值差diff比例差-0.0085\n今日ma5:1.15  ma10:1.16保持[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True]净值差diff比例差-0.0086', '易方达沪深300非银ETF512070\n今日ma10:2.32  ma20:2.34保持[False, False, False, False, False, False]净值差diff比例差-0.0085\n今日ma5:2.3  ma10:2.32保持[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]净值差diff比例差-0.0086', '160416\n今日ma10:0.96  ma20:0.96保持[False, False, False, False, False, False]净值差diff比例差0.0\n今日ma5:0.95  ma10:0.96保持[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]净值差diff比例差-0.0104', '501018\n今日ma10:0.72  ma20:0.72保持[False, False, False, False, False, False]净值差diff比例差0.0\n今日ma5:0.71  ma10:0.72保持[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]净值差diff比例差-0.0139', '162411\n今日ma10:0.4  ma20:0.4保持[False, False, False, False, False, False]净值差diff比例差0.0\n今日ma5:0.39  ma10:0.4保持[False, False, False, False, True, True, True, False, False, False, False, False, False, False, False, False]净值差diff比例差-0.025', '汇添富中证能源ETF159930\n今日ma10:0.69  ma20:0.69保持[False, False, False, False, False, False]净值差diff比例差0.0\n今日ma5:0.69  ma10:0.69保持[False, False, False, False, True, True, True, True, False, False, False, False, False, False, False, False]净值差diff比例差0.0', '国联安上证商品ETF510170\n今日ma10:2.61  ma20:2.61保持[False, False, False, False, False, False]净值差diff比例差0.0\n今日ma5:2.63  ma10:2.61保持[True, True, True, True, True, True, True, False, False, False, False, False, False, False, True, True]净值差diff比例差0.0077', '南方中证房地产ETF512200\n今日ma10:0.84  ma20:0.85保持[False, False, False, False, False, False]净值差diff比例差-0.0118\n今日ma5:0.84  ma10:0.84保持[False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True]净值差diff比例差0.0', '广发中证传媒ETF512980\n今日ma10:0.8  ma20:0.8保持[False, False, False, False, False, False]净值差diff比例差0.0\n今日ma5:0.8  ma10:0.8保持[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]净值差diff比例差0.0', '鹏华中证传媒ETF159805\n今日ma10:1.02  ma20:1.02保持[False, False, False, False, False, False]净值差diff比例差0.0\n今日ma5:1.03  ma10:1.02保持[True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False]净值差diff比例差0.0098', '华宝中证银行ETF512800\n今日ma10:1.25  ma20:1.25保持[False, False, False, False, False, False]净值差diff比例差0.0\n今日ma5:1.24  ma10:1.25保持[False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True]净值差diff比例差-0.008', '华夏中小企业100ETF159902\n今日ma10:4.42  ma20:4.41可买净值差diff比例差0.0023\n今日ma5:4.41  ma10:4.42可卖净值差diff比例差-0.0023', '华安上证180ETF510180\n今日ma10:4.19  ma20:4.18可买净值差diff比例差0.0024\n今日ma5:4.18  ma10:4.19可卖净值差diff比例差-0.0024', '510900\n今日ma10:1.2  ma20:1.21保持[False, False, False, False, False, False]净值差diff比例差-0.0083\n今日ma5:1.2  ma10:1.2可卖净值差diff比例差0.0', '159920\n今日ma10:1.51  ma20:1.51保持[False, False, False, False, False, False]净值差diff比例差0.0\n今日ma5:1.51  ma10:1.51可卖净值差diff比例差0.0', '164906\n今日ma10:2.0  ma20:2.06保持[False, False, False, False, False, False]净值差diff比例差-0.0291\n今日ma5:2.02  ma10:2.0保持[True, True, True, True, False, False, False, False, False, False, False, False, False, True, True, True]净值差diff比例差0.01', '513050\n今日ma10:2.07  ma20:2.09保持[False, False, False, False, False, False]净值差diff比例差-0.0096\n今日ma5:2.08  ma10:2.07保持[True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False]净值差diff比例差0.0048', '鹏华中证酒ETF512690\n今日ma10:2.43  ma20:2.35保持[True, True, True, True, True, True]净值差diff比例差0.034\n今日ma5:2.43  ma10:2.43可卖净值差diff比例差0.0']
    for i in jjc:
        jj, jj_jin = getJijin(i.strip())
        name = ''
        jjcode = i
        if jj != False:
            name = jj['name']
        jj_content = get_single_etf_report(jjcode,name)
        content.append(jj_content)
    sorted(content, key=functools.cmp_to_key(cmp))
    content = '\n\n\n'.join(content)
    mailsender=MailSender(my_sender, my_pass, sender_name, receiver_addr, subject, content,None)
    mailsender.send_it()


get_buy_and_sell_etf()