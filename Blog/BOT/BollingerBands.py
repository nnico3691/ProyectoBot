import pandas as pd
from ta.utils import dropna
from ta.volatility import BollingerBands


# DEFINICION
# Indicadores que informarán del momento en que el valor de cierre tiene:
# 1) un valor mayor que la banda superior de Bollinger
# 2) Un valor menor que la banda inferior de Bollinger.
# Resultado: Por tanto, estas dos características normalmente valdrán 0 excepto cuando el valor de cierre sale de estas, que valdrá 1.
# Conclusion: Normalmente conviene VENDER cuando supera la banda por arriba y COMPRAR cuando es menor que la banda inferior.

def addBollingerBands(data):
    # Clean NaN values
    data = dropna(data)

    # Initialize Bollinger Bands Indicator
    indicator_bb = BollingerBands(close=data["Close"], window=20, window_dev=2)

    # Add Bollinger Bands features
    data['bb_bbm'] = indicator_bb.bollinger_mavg()
    data['bb_bbh'] = indicator_bb.bollinger_hband()
    data['bb_bbl'] = indicator_bb.bollinger_lband()

    # Add Bollinger Band high indicator
    data['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()

    # Add Bollinger Band low indicator
    data['bb_bbli'] = indicator_bb.bollinger_lband_indicator()

    return data
