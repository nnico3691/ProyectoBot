from datetime import datetime
from datetime import date
from datetime import timedelta

import calendar
import locale

import holidays


def VerificarFecha(Fecha):
    FechaReturn = Fecha

    ar_argentina = holidays.Argentina()
    if Fecha in ar_argentina:
        FechaReturn = FechaReturn - timedelta(days=1)

    # Si es Domingo
    if FechaReturn.weekday() == 6:
        FechaReturn = FechaReturn - timedelta(days=2)

    # Si es Sábado:
    if FechaReturn.weekday() == 5:
        FechaReturn = FechaReturn - timedelta(days=1)

    if FechaReturn in ar_argentina:
        FechaReturn = FechaReturn - timedelta(days=1)

    return FechaReturn


fechaPrueba = datetime.strptime('2022-08-15', '%Y-%m-%d')
ar_holidays=holidays.Argentina()
for i in holidays.Argentina(years=2022).items():
    print(i)

print(VerificarFecha(fechaPrueba))

locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")

today = datetime.strptime('2022-01-01', '%Y-%m-%d')
yesterday = today - timedelta(days=2)
today5Dias = today - timedelta(days=5)
print(today5Dias)
if today5Dias < yesterday:
    print('Entre')

print("==========PRUEBA==========")
# asigna fecha actual
hoy = date.today()
# suma a fecha actual 1 dia
ayer = hoy + timedelta(days=-1)
# diferencia
diferencia_en_dias = hoy - ayer
print(print(diferencia_en_dias.days - 1))


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

print(ListaTicker.pop()["Ticker"])

# for registro in ListaTicker:
#    print(registro["Ticker"])



Cartera = 30000