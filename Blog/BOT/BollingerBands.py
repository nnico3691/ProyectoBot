import pandas as pd
from ta.utils import dropna
from ta.volatility import BollingerBands

import yfinance as yf

# DEFINICION
# En la biblioteca, este indicador es transformado en 5 características.
# Porque además de las 3 características resultantes de las 3 bandas ya mencionadas, generamos otros 2
# indicadores que informarán del momento en que el valor de
# cierre tiene un valor mayor que la banda superior de Bollinger o menor que la banda inferior de Bollinger. Por tanto, estas dos
# características normalmente valdrán 0 excepto cuando el valor de cierre sale de estas, que valdrá 1.

# Normalmente conviene vender cuando supera la banda por arriba y comprar cuando es menor que la banda inferior.

# Load datas
# df = pd.read_csv(f'E:/Proyectos/Python/Proyecto Bot/ta-master/test/data/datas.csv', sep=',')
df = yf.download('BTC-USD', period='1d', start="2022-01-01", end="2022-11-16")

# Clean NaN values
df = dropna(df)

# Initialize Bollinger Bands Indicator
indicator_bb = BollingerBands(close=df["Close"], window=20, window_dev=2)

# Add Bollinger Bands features
df['bb_bbm'] = indicator_bb.bollinger_mavg()
df['bb_bbh'] = indicator_bb.bollinger_hband()
df['bb_bbl'] = indicator_bb.bollinger_lband()

# Add Bollinger Band high indicator
df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()

# Add Bollinger Band low indicator
df['bb_bbli'] = indicator_bb.bollinger_lband_indicator()

filtroHI = df['bb_bbhi'] == 1.0
filtroLI = df['bb_bbli'] == 1.0

dPruebaHI = df[filtroHI]
dPruebaLI = df[filtroLI]
print(dPruebaLI)
print(dPruebaHI)


