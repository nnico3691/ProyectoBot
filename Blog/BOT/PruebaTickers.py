import yfinance as yf

start = "2022-10-01"
end = "2022-11-01"

# pull data from Yahoo Finance
data = yf.download('AAPL', interval='5m',  start=start, end=end)
print(data)