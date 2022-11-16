import BollingerBands as bl
import RSI as rs

import yfinance as yf

# pull data from Yahoo Finance
data = yf.download('BTC-USD', period='1d', start="2022-01-01", end="2022-11-16")
data = rs.addRSI(data)
data = bl.addBollingerBands(data)

data.to_csv(r'E:/Proyectos/Python/Proyecto Bot/Prueba.csv', index=False)

