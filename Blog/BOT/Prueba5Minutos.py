import BollingerBands as bl
import RSI as rs

import ta
from ta.utils import dropna
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

from datetime import datetime
from datetime import date
from datetime import timedelta

start = "2022-10-01"
end = "2022-11-18"
ticker = 'CEPU.BA'

data = yf.download(ticker, interval='5m', period='1d')
data = bl.addBollingerBands(data)
data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=14).rsi()

filtro = (data['bb_bbli'] == 1.0) | (data['bb_bbhi'] == 1.0)
filtro = (data['bb_bbli'] == 1.0) & (data['RSI'] < 30) | (data['bb_bbhi'] == 1.0) & (data['RSI'] > 70)

df = data[filtro]

for date, row in df.T.items():
    print(date)


data2 = yf.download('CEPU.BA', interval='5m', period='1d')

print(data2.tail(1))

