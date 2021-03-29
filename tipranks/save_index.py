import bs4 as bs
import datetime as dt
import os
# import pandas_datareader.data as web
# import pickle
import requests
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}

# https://www.slickcharts.com/sp500 dowjones etf/ark-invest/ARKW
def save_tickers(index):
    resp = requests.get('https://www.slickcharts.com/'+index, headers=headers)
    soup = bs.BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table', {'class': 'table'})
    tickers = []
    symbols = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[1].text
        tickers.append(ticker)
        symbol = row.findAll('td')[2].text
        symbols.append(symbol)
    return tickers, symbols


def save_all_index():
    indexs = ['nasdaq100','sp500', 'dowjones', 'etf/ark-invest/ARKW']
    all_tickers = []
    all_symbols = []
    for index in indexs:
        tickers, symbols = save_tickers(index)
        all_tickers +=tickers
        all_symbols += symbols
    df = pd.DataFrame()
    df['Ticker'] = all_symbols
    df['ticker_name'] = all_tickers
    df_clean = df.drop_duplicates(subset=['Ticker'])
    df_clean.to_csv('all_index.csv', index=None)


save_all_index()