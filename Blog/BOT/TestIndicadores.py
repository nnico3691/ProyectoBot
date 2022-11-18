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

print("======COMIENZO=====")

start = "2022-01-01"
end = "2022-11-18"

ListaTicker = [{"Ticker": 'GOLD', "CarteraTicker": 15000},
               {"Ticker": 'TSLA.BA', "CarteraTicker": 15000},
               {"Ticker": 'AAPL.BA', "CarteraTicker": 15000},
               {"Ticker": 'CEPU.BA', "CarteraTicker": 3000},
               {"Ticker": 'VALO.BA', "CarteraTicker": 5000},
               {"Ticker": 'SUPV.BA', "CarteraTicker": 5000},
               {"Ticker": 'PAMP.BA', "CarteraTicker": 5000},
               {"Ticker": 'GGAL.BA', "CarteraTicker": 5000}]

for registro in ListaTicker:

    ticker = registro["Ticker"]

    print("======== INICIO ANALISIS TIKCER " + ticker + "========")

    # pull data from Yahoo Finance
    data = yf.download(ticker, period='1d', start=start, end=end)

    data = bl.addBollingerBands(data)

    # data['RSI'] = rs.RSI(data, 7)
    data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=9).rsi()

    data['RSI'].plot()
    data['Adj Close'].plot()

    fig, axes = plt.subplots(2, 1)
    axes[0].plot(data['Adj Close'], color='black')
    axes[1].plot(data['RSI'], color='b')

    axes[0].set_title('Precio BTC')
    axes[1].set_title('RSI')
    axes[1].axhline(y=30, color='r', linewidth=3)
    axes[1].axhline(y=70, color='r', linewidth=3)
    plt.tight_layout()
    fig.autofmt_xdate()

    # filtro = ((data['bb_bbli'] == 1.0) & data['RSI'] < 30) | ((data['bb_bbhi'] == 1.0) & data['RSI'] > 70)
    filtro = (data['bb_bbli'] == 1.0) | (data['bb_bbhi'] == 1.0)
    filtro = (data['bb_bbli'] == 1.0) & (data['RSI'] < 30) | (data['bb_bbhi'] == 1.0) & (data['RSI'] > 70)

    # plt.show()

    df = data[filtro]

    Inversion = [{
        "Cartera": 100000,
        "Cantidad": 0,
        "Fecha": '',
        "Precio": 0.0,
        'Total': 100000,
        "TipoOp": 'Inicio'
    }]

    Cartera = 100000
    Cantidad = 0
    bb_bbli = 1
    bb_bbhi = 1
    CompraInicial = 0
    VentaInicial = 0
    fechaAnt = datetime.strptime(start, '%Y-%m-%d')

    for date, row in df.T.items():

        month = str(date.month)
        if len(month) == 1:
            month = '0' + month

        fechaActual = datetime.strptime(str(date.year) + '-' + month + '-' + str(date.day), '%Y-%m-%d')
        fecha5Dias = datetime.strptime(str(date.year) + '-' + month + '-' + str(date.day), '%Y-%m-%d') - timedelta(
            days=5)

        if fecha5Dias > fechaAnt:
            if VentaInicial == 1:
                bb_bbhi = 0
            if CompraInicial == 1:
                bb_bbli = 0

        if (row['bb_bbli'] == 1.0) & (row['RSI'] <= 30) & (Cartera >= row['Adj Close']):
            if bb_bbli == 1:
                Cartera = Cartera - row['Adj Close']
                Cantidad = Cantidad + 1
                Inversion += [{
                    "Cartera": Cartera,
                    "Cantidad": Cantidad,
                    "Fecha": str(date.year) + '-' + month + '-' + str(date.day),
                    "Precio": row['Adj Close'],
                    'Total': Cartera + Cantidad * row['Adj Close'],
                    "TipoOp": 'COMPRA'
                }]

                CompraInicial = 1
            else:
                bb_bbli = 1

        if (row['bb_bbhi'] == 1.0) & (row['RSI'] >= 70) & (Cantidad > 0):
            if bb_bbhi == 1:
                Multiplicador = 1
                if Cantidad > 1:
                    Multiplicador = 2

                Cartera = Cartera + (row['Adj Close'] * Multiplicador)
                Cantidad = Cantidad - Multiplicador
                Inversion += [{
                    "Cartera": Cartera,
                    "Cantidad": Cantidad,
                    "Fecha": str(date.year) + '-' + month + '-' + str(date.day),
                    "Precio": row['Adj Close'],
                    'Total': Cartera + Cantidad * row['Adj Close'],
                    "TipoOp": 'VENTA'
                }]

                VentaInicial = 1
            else:
                bb_bbhi = 1

        fechaAnt = fechaActual

    for i in Inversion:
        print(i)

    print("======== FIN ANALISIS TICkER " + ticker + "========")

# data.to_csv(r'E:/Proyectos/Python/Proyecto Bot/Archivos/GOLD.csv', index=False)
