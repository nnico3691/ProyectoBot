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

ListaTicker = [
    {"Ticker": 'AAPL.BA', "CarteraTicker": 100000},
    {"Ticker": 'AMZN.BA', "CarteraTicker": 100000},
    # {"Ticker": 'BTC-USD', "CarteraTicker": 200000},
    {"Ticker": 'CEPU.BA', "CarteraTicker": 30000},
    {"Ticker": 'GGAL.BA', "CarteraTicker": 50000},
    # {"Ticker": 'GOLD', "CarteraTicker": 15000},
    {"Ticker": 'KO.BA', "CarteraTicker": 100000},
    {"Ticker": 'MELI.BA', "CarteraTicker": 15000},
    {"Ticker": 'MSFT.BA', "CarteraTicker": 50000},
    {"Ticker": 'PAMP.BA', "CarteraTicker": 30000},
    {"Ticker": 'SUPV.BA', "CarteraTicker": 15000},
    {"Ticker": 'TSLA.BA', "CarteraTicker": 100000},
    {"Ticker": 'VALO.BA', "CarteraTicker": 13000}
]

for registro in ListaTicker:

    ticker = registro["Ticker"]
    Cartera = registro["CarteraTicker"]

    print("======== INICIO ANALISIS TICkER " + ticker + "========")

    # pull data from Yahoo Finance
    data = yf.download(ticker, period='1d', start=start, end=end)

    data = bl.addBollingerBands(data)

    # data['RSI'] = rs.RSI(data, 7)
    data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=14).rsi()

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
        "Cartera": Cartera,
        "Cantidad": 0,
        "Fecha": '',
        "Precio": 0.0,
        'Total': Cartera,
        "TipoOp": 'Inicio'
    }]

    Cantidad = 0
    bb_bbli = 1
    bb_bbhi = 1
    CompraInicial = 0
    VentaInicial = 0
    fechaAnt = datetime.strptime(start, '%Y-%m-%d')
    CantidadCompra = 0
    CantidadCompraAux = 0

    for date, row in df.T.items():

        if CantidadCompra == 0:
            CantidadCompra = int((Cartera / row['Adj Close']) * 0.4)
            CantidadCompraAux = CantidadCompra

        if CantidadCompra == 0:
            CantidadCompra = 1

        month = str(date.month)
        if len(month) == 1:
            month = '0' + month

        day = str(date.day)
        if len(day) == 1:
            day = '0' + day

        fechaActual = datetime.strptime(str(date.year) + '-' + month + '-' + day, '%Y-%m-%d')
        fecha5Dias = datetime.strptime(str(date.year) + '-' + month + '-' + day, '%Y-%m-%d') - timedelta(
            days=5)

        if fecha5Dias > fechaAnt:
            if VentaInicial == 1:
                bb_bbhi = 0
            if CompraInicial == 1:
                bb_bbli = 0

        if Cartera <= (row['Adj Close'] * CantidadCompra):
            CantidadCompra = int(CantidadCompra/2)

        if CantidadCompra == 0:
            CantidadCompra = 1

        if (row['bb_bbli'] == 1.0) & (row['RSI'] <= 30) & (Cartera >= (row['Adj Close'] * CantidadCompra)):
            if bb_bbli == 1:
                Cartera = Cartera - (row['Adj Close'] * CantidadCompra)
                Cantidad = Cantidad + CantidadCompra
                Inversion += [{
                    "Cartera": Cartera,
                    "Cantidad": Cantidad,
                    "Fecha": str(date.year) + '-' + month + '-' + day,
                    "Precio": row['Adj Close'],
                    'Total': Cartera + Cantidad * row['Adj Close'],
                    "TipoOp": 'COMPRA'
                }]

                CompraInicial = 1
            else:
                bb_bbli = 1

        Multiplicador = 4
        CantidadVenta = 1
        if Cantidad >= (CantidadCompraAux * Multiplicador):
            CantidadVenta = CantidadCompraAux * Multiplicador
        else:
            CantidadVenta = CantidadCompraAux

        if Cantidad < CantidadCompraAux:
            CantidadVenta = Cantidad

        if (row['bb_bbhi'] == 1.0) & (row['RSI'] >= 70) & (Cantidad >= CantidadVenta) & (Cantidad > 0):
            if bb_bbhi == 1:

                Cartera = Cartera + (row['Adj Close'] * CantidadVenta)
                Cantidad = Cantidad - CantidadVenta
                Inversion += [{
                    "Cartera": Cartera,
                    "Cantidad": Cantidad,
                    "Fecha": str(date.year) + '-' + month + '-' + day,
                    "Precio": row['Adj Close'],
                    'Total': Cartera + Cantidad * row['Adj Close'],
                    "TipoOp": 'VENTA'
                }]
                CantidadCompra = CantidadCompraAux
                VentaInicial = 1
            else:
                bb_bbhi = 1

        fechaAnt = fechaActual

    for i in Inversion:
        print(i)

    print("======== FIN ANALISIS TICkER " + ticker + "========")

# data.to_csv(r'E:/Proyectos/Python/Proyecto Bot/Archivos/GOLD.csv', index=False)
