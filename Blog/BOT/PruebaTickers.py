import yfinance as yf

start = "2022-10-01"
end = "2022-11-17"

data = yf.download('TSLA.BA', period='1d', start=start, end=end)
print(data)