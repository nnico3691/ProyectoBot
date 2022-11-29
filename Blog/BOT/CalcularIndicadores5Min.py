import BollingerBands as bl

import ta
from ta.utils import dropna
import matplotlib.pyplot as plt

from datetime import datetime
from datetime import date
from datetime import timedelta


def CalcularIndicadores5Min(CarteraTope, data, Cartera, Inversion, FechaActual, GananciaTotal,Porcentaje, AwesomeOscillattorPostive, AwesomeOscillattorNegative, RSICompraInferior, RSICompraSuperior, RSIVentaInferior):
    DineroCompras = 0
    DineroVentas = 0
    InversionActual = 0

    data = bl.addBollingerBands(data)

    data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=9).rsi()
    data['awesome_oscillator'] = ta.momentum.AwesomeOscillatorIndicator(data['High'], data['Low'], window1=5,
                                                                        window2=34,
                                                                        fillna=False).awesome_oscillator()

    filtro = (data['bb_bbli'] == 1.0) | (data['bb_bbhi'] == 1.0)
    filtro = (data['bb_bbli'] == 1.0) & (data['RSI'] <= RSICompraSuperior) | (data['bb_bbhi'] == 1.0) & (data['RSI'] >= RSIVentaInferior)

    df = data[filtro]

    df = df.loc[FechaActual:FechaActual]

    Cantidad = Inversion[-1]["CantidadTotal"]
    bb_bbli = 1
    bb_bbhi = 1
    CantidadCompra = 0
    CantidadCompraAux = 0

    for date, row in df.T.items():

        CantidadCompra = int((Cartera / row['Adj Close']) * Porcentaje)

        if CantidadCompra == 0:
            CantidadCompra = 1

        if Cartera <= (row['Adj Close'] * CantidadCompra):
            CantidadCompra = int(CantidadCompra / 2)

        if Cartera <= (row['Adj Close'] * CantidadCompra):
            CantidadCompra = int(CantidadCompra)

        if CantidadCompra == 0:
            CantidadCompra = 1

        if (row['bb_bbli'] == 1.0) & (row['RSI'] <= RSICompraSuperior) & (row['RSI'] >= RSICompraInferior) & (Cartera >= (row['Adj Close'] * CantidadCompra)) & (row['Adj Close'] != Inversion[-1]["Precio"]) & (row['awesome_oscillator'] <= AwesomeOscillattorNegative):

            if CarteraTope < (row['Adj Close'] * CantidadCompra):
                print("===== CARTERA AL TOPE =====")
                bb_bbli = 0

            if Cartera < (row['Adj Close'] * CantidadCompra):
                bb_bbli = 0

            CANTPPORW = Inversion[-1]["CANTPPORW"] + CantidadCompra
            PPORW = Inversion[-1]["PPORW"] + (row['Adj Close'] * CantidadCompra)

            PPM = PPORW / CANTPPORW

            if bb_bbli == 1:
                GananciaTotal = GananciaTotal - (row['Adj Close'] * CantidadCompra)
                Cartera = Cartera - (row['Adj Close'] * CantidadCompra)
                Cantidad = Cantidad + CantidadCompra
                Inversion += [{
                    "Fecha": str(date),
                    "Cartera": Cartera,
                    "CantidadTotal": Cantidad,
                    "Cantidad": CantidadCompra,
                    "Precio": row['Adj Close'],
                    'Total': Cartera + Cantidad * row['Adj Close'],
                    "TipoOp": 'COMPRA',
                    "PPM": PPM,
                    "PPORW": PPORW,
                    "CANTPPORW": CANTPPORW,
                    "GananciaTotal": GananciaTotal
                }]
                DineroCompras = DineroCompras + (row['Adj Close'] * CantidadCompra)
                CarteraTope = CarteraTope - (row['Adj Close'] * CantidadCompra)

            else:
                bb_bbli = 1

        CantidadVenta = int((90 * Cantidad)/100)
        if CantidadVenta == 0:
            CantidadVenta = 1

        PPM = Inversion[-1]['PPM']

        if (row['bb_bbhi'] == 1.0) & (row['RSI'] >= RSIVentaInferior) & (Cantidad >= CantidadVenta) & (Cantidad > 0) & (CantidadVenta > 0) & (row['awesome_oscillator'] >= AwesomeOscillattorPostive) & (row['Adj Close'] > PPM):

            PPM = 0
            PPORW = 0
            CANTPPORW = 0
            if Cantidad - CantidadVenta != 0:
                PPM = Inversion[-1]['PPM']
                PPORW = Inversion[-1]['PPORW']
                CANTPPORW = Inversion[-1]['CANTPPORW']

            GananciaTotal = GananciaTotal + (CantidadVenta * row['Adj Close'])
            Cartera = Cartera + (row['Adj Close'] * CantidadVenta)
            Cantidad = Cantidad - CantidadVenta
            Inversion += [{
                "Fecha": str(date),
                "Cartera": Cartera,
                "CantidadTotal": Cantidad,
                "Cantidad": CantidadVenta,
                "Precio": row['Adj Close'],
                'Total': Cartera + (Cantidad * row['Adj Close']),
                "TipoOp": 'VENTA',
                "PPM": PPM,
                "PPORW": PPORW,
                "CANTPPORW": CANTPPORW,
                "GananciaTotal": GananciaTotal
            }]

            DineroVentas = DineroVentas + (row['Adj Close'] * CantidadVenta)
            CarteraTope = CarteraTope + (row['Adj Close'] * CantidadVenta)

    CantidadIndicador = 0

    UltimoPrecio = data.tail(1)

    for date, row in UltimoPrecio.T.items():

        if (row['Adj Close'] > Inversion[-1]["PPM"]) & (
                CantidadIndicador > 0):
            GananciaTotal = GananciaTotal + (CantidadIndicador * row['Adj Close'])

            Inversion += [{
                "Fecha": str(date),
                "Cartera": Cartera + (CantidadIndicador * row['Adj Close']),
                "CantidadTotal": 0,
                "Cantidad": CantidadIndicador,
                "Precio": row['Adj Close'],
                'Total': Cartera + (CantidadIndicador * row['Adj Close']),
                "TipoOp": 'VENTA FORZADA',
                "PPM": 0,
                "GananciaTotal": GananciaTotal
            }]

            DineroVentas = DineroVentas + (row['Adj Close'] * CantidadIndicador)
            CarteraTope = CarteraTope + (row['Adj Close'] * CantidadIndicador)

    return DineroVentas, DineroCompras, InversionActual, GananciaTotal, Inversion , CarteraTope
