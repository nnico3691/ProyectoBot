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
