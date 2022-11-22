import BollingerBands as bl
import RSI as rs

import ta
from ta.utils import dropna
import matplotlib.pyplot as plt

from datetime import datetime
from datetime import date
from datetime import timedelta


def CalcularIndicadores5Min(CarteraTope, data, Cartera, Inversion, FechaActual, GananciaTotal):
    DineroCompras = 0
    DineroVentas = 0
    InversionActual = 0

    data = bl.addBollingerBands(data)

    # data['RSI'] = rs.RSI(data, 7)
    data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=9).rsi()
    data['awesome_oscillator'] = ta.momentum.AwesomeOscillatorIndicator(data['High'], data['Low'], window1=5,
                                                                        window2=34,
                                                                        fillna=False).awesome_oscillator()

    filtro = (data['bb_bbli'] == 1.0) | (data['bb_bbhi'] == 1.0)
    filtro = (data['bb_bbli'] == 1.0) & (data['RSI'] < 30) | (data['bb_bbhi'] == 1.0) & (data['RSI'] > 70)

    df = data[filtro]

    df = df.loc[FechaActual:FechaActual]

    Cantidad = Inversion[-1]["Cantidad"]
    bb_bbli = 1
    bb_bbhi = 1
    CompraInicial = 0
    VentaInicial = 0
    CantidadCompra = 0
    CantidadCompraAux = 0
    CarteraInicial = 20000
    AwesomeOsciladorCompra = 0
    AwesomeOsciladorVenta = 0
    ValorAwesomeOsciladorCompraAnt = 0
    ValorAwesomeOsciladorVentaAnt = 0
    DesactivoCompra = 0

    for date, row in df.T.items():

        if CantidadCompra == 0:
            CantidadCompra = int((Cartera / row['Adj Close']) * 0.9)
            CantidadCompraAux = CantidadCompra

        if CantidadCompra == 0:
            CantidadCompra = 1

        if Cartera <= (row['Adj Close'] * CantidadCompra):
            CantidadCompra = int(CantidadCompra / 2)

        if Cartera <= (row['Adj Close'] * CantidadCompra):
            CantidadCompra = int(CantidadCompra)

        if CantidadCompra == 0:
            CantidadCompra = 1

        if (row['bb_bbli'] == 1.0) & (row['RSI'] <= 30) & (Cartera >= (row['Adj Close'] * CantidadCompra)) & (
                row['Adj Close'] != Inversion[-1]["Precio"]) & (date.day <= 20):

            if row['awesome_oscillator'] > ValorAwesomeOsciladorCompraAnt:
                AwesomeOsciladorCompra = 1

            if row['awesome_oscillator'] < 0:
                AwesomeOsciladorVenta = 0

            if AwesomeOsciladorCompra == 0:
                bb_bbhi = 0
                ValorAwesomeOsciladorCompraAnt = row['awesome_oscillator']

            PPM = row['Adj Close']
            if Inversion[-1]["PPM"] != 0:
                PPM = (((row['Adj Close'] * CantidadCompra) / CantidadCompra) + Inversion[-1]["PPM"]) / 2

            if PPM < row['Adj Close']:
                bb_bbli = 0

            if CarteraTope < (row['Adj Close'] * CantidadCompra):
                print("===== CARTERA AL TOPE =====")
                bb_bbli = 0

            if Cartera < (row['Adj Close'] * CantidadCompra):
                bb_bbli = 0

            if (bb_bbli == 1) & (DesactivoCompra == 0):
                GananciaTotal = GananciaTotal - (row['Adj Close'] * CantidadCompra)
                Cartera = Cartera - (row['Adj Close'] * CantidadCompra)
                Cantidad = Cantidad + CantidadCompra
                Inversion += [{
                    "Fecha": str(date),
                    "Cartera": Cartera,
                    "Cantidad": Cantidad,
                    "Precio": row['Adj Close'],
                    'Total': Cartera + Cantidad * row['Adj Close'],
                    "TipoOp": 'COMPRA',
                    "PPM": PPM,
                    "GananciaTotal": Inversion[-1]["GananciaTotal"] - (row['Adj Close'] * CantidadCompra)
                }]
                DineroCompras = DineroCompras + (row['Adj Close'] * CantidadCompra)
                CompraInicial = 1
                CarteraTope = CarteraTope - (row['Adj Close'] * CantidadCompra)
                AwesomeOsciladorCompra = 0
            else:
                bb_bbli = 1

        Multiplicador = 2
        CantidadVenta = 1
        if Cantidad >= (CantidadCompraAux * Multiplicador):
            CantidadVenta = CantidadCompraAux * Multiplicador
        else:
            CantidadVenta = CantidadCompraAux

        if Cantidad < CantidadCompraAux:
            CantidadVenta = Cantidad

        if (row['bb_bbhi'] == 1.0) & (row['RSI'] >= 70) & (Cantidad >= CantidadVenta) & (Cantidad > 0) & (
                CantidadVenta > 0):

            if AwesomeOsciladorVenta == 0:
                bb_bbhi = 0
                ValorAwesomeOsciladorVentaAnt = row['awesome_oscillator']
                AwesomeOsciladorVenta = 1

            if (Inversion[-1]["TipoOp"] == 'COMPRA') & (row['Adj Close'] == Inversion[-1]["Precio"]):
                bb_bbhi = 0

            if (Inversion[-1]["TipoOp"] == 'COMPRA') & (row['Adj Close'] < Inversion[-1]["Precio"]):
                bb_bbhi = 0
                DesactivoCompra = 1

            if Inversion[-1]['PPM'] > row['Adj Close']:
                bb_bbhi == 0

            PPM = 0
            if Cantidad - CantidadVenta != 0:
                PPM = Inversion[-1]['PPM']

            if bb_bbhi == 1:

                GananciaTotal = GananciaTotal + (Cantidad * row['Adj Close'])
                Cartera = Cartera + (row['Adj Close'] * CantidadVenta)
                Cantidad = Cantidad - CantidadVenta
                Inversion += [{
                    "Fecha": str(date),
                    "Cartera": Cartera,
                    "Cantidad": Cantidad,
                    "Precio": row['Adj Close'],
                    'Total': Cartera + (Cantidad * row['Adj Close']),
                    "TipoOp": 'VENTA',
                    "PPM": PPM,
                    "GananciaTotal": Inversion[-1]["GananciaTotal"] + (Cantidad * row['Adj Close'])
                }]
                CantidadCompra = CantidadCompraAux
                VentaInicial = 1
                DineroVentas = DineroVentas + (row['Adj Close'] * CantidadVenta)
                CarteraTope = CarteraTope + (row['Adj Close'] * CantidadVenta)
                AwesomeOsciladorVenta = 0
                DesactivoCompra = 0
            else:
                bb_bbhi = 1

    CantidadIndicador = 0

    if len(Inversion) > 0:
        UltimoPrecioIndicador = Inversion[-1]["Precio"]
        CantidadIndicador = Cantidad

    UltimoPrecioIndicador2 = 0
    if len(Inversion) > 2:
        if Inversion[-2]['TipoOp'] == "COMPRA":
            UltimoPrecioIndicador2 = Inversion[-2]["Precio"]

    UltimoPrecio = data.tail(1)

    for date, row in UltimoPrecio.T.items():

        if (row['Adj Close'] > UltimoPrecioIndicador) & (row['Adj Close'] > UltimoPrecioIndicador2) & (
                CantidadIndicador > 0):
            GananciaTotal = GananciaTotal + (CantidadIndicador * row['Adj Close'])

            Inversion += [{
                "Fecha": str(date),
                "Cartera": Cartera + (CantidadIndicador * row['Adj Close']),
                "Cantidad": 0,
                "Precio": row['Adj Close'],
                'Total': Cartera + (CantidadIndicador * row['Adj Close']),
                "TipoOp": 'VENTA FORZADA',
                "PPM": 0,
                "GananciaTotal": Inversion[-1]["GananciaTotal"] + (CantidadIndicador * row['Adj Close'])
            }]

            DineroVentas = DineroVentas + (row['Adj Close'] * CantidadIndicador)
            CarteraTope = CarteraTope + (row['Adj Close'] * CantidadIndicador)

    return DineroVentas, DineroCompras, InversionActual, GananciaTotal, Inversion
