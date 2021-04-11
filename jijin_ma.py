#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
import json
import datetime
import demjson
from getInfo import today_ma

# http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=1nzf&st=desc&sd=2020-04-11&ed=2021-04-11&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.91066056957649

#  获取排名。。。按年为绩效表现。。前200名。。

#http://fund.eastmoney.com/data/fundranking.html#tall;c0;r;sqjzf;pn50;ddesc;qsd20180101;qed20190101;qdii;zq;gg;gzbd;gzfs;bbzt;sfbb  visting this page




def is_jijin_buy_opportunity(jjcode, name): 
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
    if '可买' in today_ma_info:
        return jjcode


def init():
    now = datetime.datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    last_year_date = current_date.replace(current_date[0:4],str( int(current_date[0:4]) -1)  )
    url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=1nzf&st=desc&sd='+last_year_date + '&ed='+current_date+'&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.01422445811317985'
    headers = {
        'Referer': 'https://fund.eastmoney.com/data/fundranking.html',
         'Host': 'fund.eastmoney.com', 
         'Cookie': 'ASP.NET_SessionId=1l1donc13o2ou5nax2ny34s1; path=/; HttpOnly',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    }
    jijin_list = requests.get(url, headers=headers)
    status = jijin_list.status_code
    if status != 200:
        return False
    jijin_list_json  =  jijin_list.text[14:-1]
    if not jijin_list_json:
        return False
    # https://blog.csdn.net/blueheart20/article/details/69704518
    jijin_list_info = demjson.decode(jijin_list_json)
    datas = jijin_list_info.get('datas')
    can_buy_code_list = []
    for jijin_str in datas:
        jijin = jijin_str.split(',')
        jjcode = jijin[0]
        jijin_name = jijin[1]
        if(is_jijin_buy_opportunity(jjcode, jijin_name)):
            can_buy_code_list.append(jjcode)
        print(can_buy_code_list)

    def is_jijin_match(jijin_data):
        jijin_code = jijin_data.split(',')[0]
        if jijin_code in can_buy_code_list:
            return True
        else:
            return False
    filtered_data = list(filter(is_jijin_match, datas))
    print(filtered_data)
    # filter .

init();