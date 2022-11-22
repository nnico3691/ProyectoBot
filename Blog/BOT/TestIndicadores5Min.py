import CalcularIndicadores5Min as c5min

import pandas as pd
import yfinance as yf

from datetime import datetime
from datetime import timedelta

import time
import calendar
import locale

import holidays

ListaTicker = [
    {"Ticker": 'AAPL.BA',
     "Contador": 1,
     "Inversion": [{
         "Fecha": '2022-11-01 11:00:00',
         "Cartera": 20000,
         "Cantidad": 0,
         "Precio": 0.0,
         'Total': 20000,
         "TipoOp": 'Inicio',
         "PPM": 0,
         "GananciaTotal": 0,
     }]},
    {"Ticker": 'CEPU.BA',
     "Contador": 1,
     "Inversion": [{
         "Fecha": '2022-11-01 11:00:00',
         "Cartera": 20000,
         "Cantidad": 0,
         "Precio": 0.0,
         'Total': 10000,
         "TipoOp": 'Inicio',
         "PPM": 0,
         "GananciaTotal": 0,
     }]}
    # {"Ticker": 'CEPU.BA', "CarteraTicker": 50000},
    # {"Ticker": 'COME.BA', "CarteraTicker": 50000},
    # {"Ticker": 'EDN.BA', "CarteraTicker": 50000},
    # {"Ticker": 'GGAL.BA', "CarteraTicker": 50000},
    # {"Ticker": 'KO.BA', "CarteraTicker": 40000},
    # {"Ticker": 'MELI.BA', "CarteraTicker": 20000},
    # {"Ticker": 'MSFT.BA', "CarteraTicker": 20000},
    # {"Ticker": 'PAMP.BA', "CarteraTicker": 20000},
    # {"Ticker": 'SUPV.BA', "CarteraTicker": 20000},
    # {"Ticker": 'TECO2.BA', "CarteraTicker": 20000},
    # {"Ticker": 'TSLA.BA', "CarteraTicker": 20000},
    # {"Ticker": 'VALO.BA', "CarteraTicker": 2000},
    # {"Ticker": 'YPFD.BA', "CarteraTicker": 20000},
]

CarteraTope = 60000

DineroCompras = 0
DineroVentas = 0
InversionActual = 0

date_format_str = "%Y-%m-%d %H:%M:%S"
FechaActual = datetime.strptime('2022-11-01 11:00:00', date_format_str)
FechaCorte = datetime.strptime('2022-11-20 10:00:00', date_format_str)

while FechaActual < FechaCorte:

    for registro in ListaTicker:

        ticker = registro["Ticker"]

        Inversion = registro["Inversion"]
        Cartera = Inversion[-1]["Cartera"]
        GananciaTotal = Inversion[-1]["GananciaTotal"]

        FechaTicker = Inversion[-1]["Fecha"]

        # pull data from Yahoo Finance
        data = yf.download(ticker, interval='5m', period='60d')
        data = data.loc['2022-01-01 11:00:00': FechaActual]

        if CarteraTope < Cartera:
            Cartera = CarteraTope

        if FechaActual > datetime.strptime(FechaTicker, date_format_str):
            print("====== FECHA: " + str(
                FechaActual) + " TICKER: " + ticker + "===================================================================")
            retorno = c5min.CalcularIndicadores5Min(CarteraTope, data, Cartera, Inversion, str(FechaActual), GananciaTotal)

            DineroVentas = DineroVentas + retorno[0]
            DineroCompras = DineroCompras + retorno[1]
            InversionActual = InversionActual + retorno[2]
            GananciaTotal = retorno[3]

            if registro["Contador"] != len(Inversion):

                registro["Contador"] = len(Inversion)
                for i in Inversion:
                    print(i)
            else:
                print("TICKER: " + ticker + " Cantidad: " + str(Inversion[-1]["Cantidad"]) + " PPM: " + str(Inversion[-1]["PPM"]))

    # Given timestamp in string
    time_str = str(FechaActual)

    # create datetime object from timestamp string
    given_time = datetime.strptime(time_str, date_format_str)

    n = 5
    # Add 15 minutes to datetime object
    FechaActual = given_time + timedelta(minutes=n)

    days = 0
    # Si es Domingo
    if FechaActual.weekday() == 6:
        days = 1

    # Si es Sábado:
    if FechaActual.weekday() == 5:
        days = 2

    hora = FechaActual.strftime("%H:%M:%S")
    if hora > '18:00:00':
        days = 1

    if days > 0:
        FechaActual = given_time + timedelta(days=days)
        FechaActual = datetime.strptime(str(FechaActual)[0:10] + " 11:00:00", date_format_str)

print("Dinero Ventas: " + str(DineroVentas))
print("Dinero Compras: " + str(DineroCompras))
print("Dinero Invertido Actualmente: " + str(InversionActual))
print("Ganancias: " + str(GananciaTotal))
