# import flask
import requests
import json
from mail_sender import MailSender
from getInfo import getGegu, getJijin
from readTxt import GetData

import datetime
now = datetime.datetime.now()


my_sender = '1262010981@qq.com'
my_pass = 'nrrejsviolzpjchd'
receiver_addr = ['zhangolve@gmail.com']
sender_name = 'FundCalculator'
subject = 'MonthlyFundReport ' + now.strftime("%Y-%m-%d %H:%M:%S")

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
    diff = round(first_day_value-last_day_value, 4)
    monthly_zhangfu = round(diff/last_day_value, 4) 
    content = name + jjcode_value + '\n' + first_day_day + ':'+ str(first_day_value) + '\n' + last_day_day + ':'+ str(last_day_value) + '\n' + '20个交易日共收益' + str(monthly_zhangfu)
    return content
   

def get_monthly_report():
    d = GetData()
    jjc = d.getJjCode()
    content = []
    for i in jjc:
        jj, jj_jin = getJijin(i.strip())
        name = ''
        jjcode = i
        if jj != False:
            name, guzhi, gutime = jj['name'], jj['gszzl'] + '%', jj['gztime']
        jj_content = get_single_monthly_report(jjcode,name)
        content.append(jj_content)
    content = '\n\n\n'.join(content)
    print(content)
    mailsender=MailSender(my_sender, my_pass, sender_name, receiver_addr, subject, content)
    mailsender.send_it()


get_monthly_report()

