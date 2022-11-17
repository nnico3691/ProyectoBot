import BollingerBands as bl
import RSI as rs
import matplotlib.pyplot as plt
import yfinance as yf
from ta.utils import dropna

# pull data from Yahoo Finance
data = yf.download('BTC-USD', period='1d', start="2022-01-01", end="2022-11-16")
data = bl.addBollingerBands(data)

rs.RSI(data, n=14)

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


print(data[filtro])
plt.show()

print("FINALIZACION")
# data = rs.addRSI(data)
# data.to_csv(r'E:/Proyectos/Python/Proyecto Bot/Prueba.csv', index=False)
