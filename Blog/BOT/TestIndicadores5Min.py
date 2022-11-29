import CalcularIndicadores5Min as c5min

import pandas as pd
import yfinance as yf

from datetime import datetime
from datetime import timedelta

import time
import calendar
import locale

import holidays

from Archivo import Archivo

import BollingerBands as bl
import ta

ListaTicker = [
    {"Ticker": 'AAPL.BA',
     "Contador": 1,
     "Porcentaje": 0.7,
     "AwesomeOscillattorPostive": 27.00,
     "AwesomeOscillattorNegative": -20.00,
     "RSICompraInferior": 25.00,
     "RSICompraSuperior": 30.00,
     "RSIVentaInferior": 75.00,
     "Inversion": [{
         "Fecha": '2022-11-01 11:00:00',
         "Cartera": 75000,
         "CantidadTotal": 0,
         "Cantidad": 0,
         "Precio": 0.0,
         'Total': 75000,
         "TipoOp": 'Inicio',
         "PPM": 0,
         "PPORW": 0,
         "CANTPPORW": 0,
         "GananciaTotal": 0,
     }]
     },
    {"Ticker": 'CEPU.BA',
     "Contador": 1,
     "Porcentaje": 0.6,
     "AwesomeOscillattorPostive": 1.8,
     "AwesomeOscillattorNegative": -0.5,
     "RSICompraInferior": 25.00,
     "RSICompraSuperior": 30.00,
     "RSIVentaInferior": 75.00,
     "Inversion": [{
         "Fecha": '2022-11-01 11:00:00',
         "Cartera": 15000,
         "CantidadTotal": 0,
         "Cantidad": 0,
         "Precio": 0.0,
         'Total': 15000,
         "TipoOp": 'Inicio',
         "PPM": 0,
         "PPORW": 0,
         "CANTPPORW": 0,
         "GananciaTotal": 0,
     }]},
    {"Ticker": 'KO.BA',
     "Contador": 1,
     "Porcentaje": 0.7,
     "AwesomeOscillattorPostive": 27.00,
     "AwesomeOscillattorNegative": -25.00,
     "RSICompraInferior": 27.00,
     "RSICompraSuperior": 30.00,
     "RSIVentaInferior": 75.00,
     "Inversion": [{
         "Fecha": '2022-11-01 11:00:00',
         "Cartera": 35000,
         "CantidadTotal": 0,
         "Cantidad": 0,
         "Precio": 0.0,
         'Total': 35000,
         "TipoOp": 'Inicio',
         "PPM": 0,
         "PPORW": 0,
         "CANTPPORW": 0,
         "GananciaTotal": 0,
     }]},
    {"Ticker": 'YPFD.BA',
     "Contador": 1,
     "Porcentaje": 0.7,
     "AwesomeOscillattorPostive": 35.00,
     "AwesomeOscillattorNegative": -15.00,
     "RSICompraInferior": 25.00,
     "RSICompraSuperior": 30.00,
     "RSIVentaInferior": 75.00,
     "Inversion": [{
         "Fecha": '2022-11-01 11:00:00',
         "Cartera": 45000,
         "CantidadTotal": 0,
         "Cantidad": 0,
         "Precio": 0.0,
         'Total': 45000,
         "TipoOp": 'Inicio',
         "PPM": 0,
         "PPORW": 0,
         "CANTPPORW": 0,
         "GananciaTotal": 0,
     }]},
    {"Ticker": 'TSLA.BA',
     "Contador": 1,
     "Porcentaje": 0.6,
     "AwesomeOscillattorPostive": 30.00,
     "AwesomeOscillattorNegative": -15.00,
     "RSICompraInferior": 25.00,
     "RSICompraSuperior": 30.00,
     "RSIVentaInferior": 75.00,
     "Inversion": [{
         "Fecha": '2022-11-01 11:00:00',
         "Cartera": 60000,
         "CantidadTotal": 0,
         "Cantidad": 0,
         "Precio": 0.0,
         'Total': 60000,
         "TipoOp": 'Inicio',
         "PPM": 0,
         "PPORW": 0,
         "CANTPPORW": 0,
         "GananciaTotal": 0,
     }]},
    {"Ticker": 'NVDA.BA',
     "Contador": 1,
     "Porcentaje": 0.7,
     "AwesomeOscillattorPostive": 35.00,
     "AwesomeOscillattorNegative": -15.00,
     "RSICompraInferior": 25.00,
     "RSICompraSuperior": 30.00,
     "RSIVentaInferior": 75.00,
     "Inversion": [{
         "Fecha": '2022-11-01 11:00:00',
         "Cartera": 55000,
         "CantidadTotal": 0,
         "Cantidad": 0,
         "Precio": 0.0,
         'Total': 55000,
         "TipoOp": 'Inicio',
         "PPM": 0,
         "PPORW": 0,
         "CANTPPORW": 0,
         "GananciaTotal": 0,
     }]},
    {"Ticker": 'ZM.BA',
     "Contador": 1,
     "Porcentaje": 0.7,
     "AwesomeOscillattorPostive": 35.00,
     "AwesomeOscillattorNegative": -15.00,
     "RSICompraInferior": 25.00,
     "RSICompraSuperior": 30.00,
     "RSIVentaInferior": 75.00,
     "Inversion": [{
         "Fecha": '2022-11-01 11:00:00',
         "Cartera": 55000,
         "CantidadTotal": 0,
         "Cantidad": 0,
         "Precio": 0.0,
         'Total': 55000,
         "TipoOp": 'Inicio',
         "PPM": 0,
         "PPORW": 0,
         "CANTPPORW": 0,
         "GananciaTotal": 0,
     }]},

    # {"Ticker": 'MELI.BA', "CarteraTicker": 20000},
    # {"Ticker": 'MSFT.BA', "CarteraTicker": 20000},
    # {"Ticker": 'PAMP.BA', "CarteraTicker": 20000},
    # {"Ticker": 'SUPV.BA', "CarteraTicker": 20000},
    # {"Ticker": 'TECO2.BA', "CarteraTicker": 20000},
]

CarteraTope = 300000

DineroCompras = 0
DineroVentas = 0
InversionActual = 0

date_format_str = "%Y-%m-%d %H:%M:%S"
FechaActual = datetime.strptime('2022-11-29 11:00:00', date_format_str)
FechaCorte = datetime.strptime('2022-11-29 18:05:00', date_format_str)

FechaTicker = '2022-08-30 11:00:00'

flagPrueba = 1
if flagPrueba == 1:
    for registro in ListaTicker:
        ticker = registro["Ticker"]

        data = yf.download(ticker, interval='5m', period='60d')
        data = bl.addBollingerBands(data)

        data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=9).rsi()
        data['awesome_oscillator'] = ta.momentum.AwesomeOscillatorIndicator(data['High'], data['Low'], window1=5,
                                                                            window2=34,
                                                                            fillna=False).awesome_oscillator()

        filtro = (data['bb_bbli'] == 1.0) | (data['bb_bbhi'] == 1.0)
        filtro = (data['bb_bbli'] == 1.0) & (data['RSI'] < 30) | (data['bb_bbhi'] == 1.0) & (data['RSI'] > 70)

        df = data[filtro]

        Fecha = datetime.today().strftime('%Y-%m-%d')

        URL = "E:/Proyectos/Python/Proyecto Bot/Blog/BOT/Logs/" + ticker + "_" + Fecha + ".csv"
        df.to_csv(URL)

flagCircuito = 1

if flagCircuito == 1:
    while FechaActual <= FechaCorte:

        for registro in ListaTicker:

            ticker = registro["Ticker"]

            AwesomeOscillattorPostive = registro["AwesomeOscillattorPostive"]
            AwesomeOscillattorNegative = registro["AwesomeOscillattorNegative"]

            RSICompraInferior = registro["RSICompraInferior"]
            RSICompraSuperior = registro["RSICompraSuperior"]
            RSIVentaInferior = registro["RSIVentaInferior"]

            Inversion = registro["Inversion"]
            Cartera = Inversion[-1]["Cartera"]
            GananciaTotal = Inversion[-1]["GananciaTotal"]
            Porcentaje = registro["Porcentaje"]

            # pull data from Yahoo Finance
            data = yf.download(ticker, interval='5m', period='60d')
            data = data.loc['2022-01-01 11:00:00': FechaActual]

            if CarteraTope < Cartera:
                Cartera = CarteraTope

            if FechaActual > datetime.strptime(FechaTicker, date_format_str):

                retorno = c5min.CalcularIndicadores5Min(CarteraTope, data, Cartera, Inversion, str(FechaActual),
                                                        GananciaTotal, Porcentaje, AwesomeOscillattorPostive,
                                                        AwesomeOscillattorNegative,
                                                        RSICompraInferior, RSICompraSuperior, RSIVentaInferior)

                DineroVentas = DineroVentas + retorno[0]
                DineroCompras = DineroCompras + retorno[1]
                InversionActual = InversionActual + retorno[2]
                GananciaTotal = retorno[3]
                CarteraTope = retorno[5]

                # if registro["Contador"] != len(Inversion):

                # registro["Contador"] = len(Inversion)
                print("\n")
                print("\n")

                print("============================== TICkER: " + ticker + " FECHA:" + str(
                    FechaActual) + " ==============================")
                print("============================== Disponible: " + str(
                    CarteraTope) + " ==============================")
                for i in Inversion:
                    Fecha = datetime.today().strftime('%Y-%m-%d')

                    URL = "E:/Proyectos/Python/Proyecto Bot/Blog/BOT/Logs/Circuito" + Fecha + ".txt"

                    print(i)
                    # Archivo.Write("TICKER: " + ticker + " ," + str(i) + " \n", URL)

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

    for registro in ListaTicker:
        Inversion = registro["Inversion"]
        Ticker = registro["Ticker"]
        GananciaTotal = Inversion[-1]["GananciaTotal"]
        PPM = Inversion[-1]["PPM"]

        print(
            "===============================================================================================================")
        print("TICKER: " + Ticker + " GANANCIAS: " + str(GananciaTotal) + " Cantidad: " + str(
            Inversion[-1]["CantidadTotal"]) + " PPM: " + str(PPM))
