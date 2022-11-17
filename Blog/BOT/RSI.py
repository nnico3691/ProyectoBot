# load packages
import pandas as pd
from ta.utils import dropna
from ta import add_all_ta_features
from ta.momentum import RSIIndicator

import yfinance as yf


def addRSI(data):
    # Clean NaN values
    data = dropna(data)

    rsi_21 = RSIIndicator(close=data['Adj Close'], window=21)
    rsi_14 = RSIIndicator(close=data['Adj Close'], window=14)

    data["rsi_14"] = rsi_14.rsi()
    data["rsi_21"] = rsi_21.rsi()

    return data


# DEFINICION
# Se trata de un indicador técnico que se utiliza para medir la fuerza relativa de un activo y detectar su momentum

# Primer Estrategia
# Hay dos formas principales de utilizar el RSI: COMPRAR cuando el indicador está por debajo de 30 y VENDER cuando está por encima de 70,
# Segunda Estrategia
# Buscar puntos de divergencia.

def RSI(precios, n):  # Accion a calcular el RSI y n numeros de periodos n = 14

    delta = precios['Adj Close'].diff()
    delta = delta[1:]

    sube, baja = delta.copy(), delta.copy()
    sube[sube < 0] = 0
    baja[baja > 0] = 0

    # Calculamos las medias de subida y bajada
    media_sube = sube.rolling(n).mean()
    media_baja = baja.abs().rolling(n).mean()

    # Calculo fuerza relativa
    RS = media_sube / media_baja

    # Calculo índice RSI
    precios['RSI'] = 100 - (100 / (1 + RS))

    return precios['RSI']
