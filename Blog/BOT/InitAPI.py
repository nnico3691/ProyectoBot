import requests
import json

token = "pS7SXg5OFTtC8+nJbS7zXuTvdWEvcJbwqdDWK/NDkhc="


def HolaMundo():
    print("Hola Mundo")


# Conectándose a la API por token de autenticación
def PostToken():
    try:
        print("========PostToken========")

        # Agregar el cuerpo a enviar (en formato json)
        headers = {
            'X-Username': 'nnico36917609',
            'X-Password': 'epfomT3('
        }

        URL = "https://api.remarkets.primary.com.ar/auth/getToken"

        # Enviar solicitud
        req = requests.post(URL, headers=headers)
        # Aquí está la respuesta
        return req.headers.get('X-Auth-Token')
    except Exception as ex:
        print("Error durante la ejecucion del PostToken {}".format(ex))


# Segmentos: Lista de Segmentos disponibles
def GetSegmentos(XAuthToken):
    try:

        # encabezado de solicitud http
        headers = {'X-Auth-Token': XAuthToken}

        # Agregar información de encabezado http
        req = requests.get('https://api.remarkets.primary.com.ar/rest/segment/all', headers=headers)

        # Aquí está la respuesta
        response = req.text
        print(json.loads(response))

    except Exception as ex:
        print("Error durante la ejecucion del GetSegmentos {}".format(ex))


# Instrumentos: Lista de Instrumentos disponibles
def GetInstrumentos(XAuthToken):
    try:

        # encabezado de solicitud http
        headers = {'X-Auth-Token': XAuthToken}

        # Agregar información de encabezado http
        req = requests.get('https://api.remarkets.primary.com.ar/rest/instruments/all', headers=headers)

        # Aquí está la respuesta
        response = req.text
        print(json.loads(response))

    except Exception as ex:
        print("Error durante la ejecucion del GetSegmentos {}".format(ex))


#  Instrumentos: Lista Detallada de Instrumentos disponibles
def GetInstrumentosDetalle(XAuthToken):
    try:

        # encabezado de solicitud http
        headers = {'X-Auth-Token': XAuthToken}

        # Agregar información de encabezado http
        req = requests.get('https://api.remarkets.primary.com.ar/rest/instruments/details', headers=headers)

        # Aquí está la respuesta
        response = req.text
        print(json.loads(response))

    except Exception as ex:
        print("Error durante la ejecucion del GetSegmentos {}".format(ex))


# Instrumentos: Descripción detallada de un Instrumento
def GetInstrumentoDetalle(XAuthToken, marketId, symbol):
    try:

        # encabezado de solicitud http
        headers = {'X-Auth-Token': XAuthToken}

        params = {
            'marketId': marketId,
            'symbol': symbol
        }

        # Agregar información de encabezado http
        req = requests.get('https://api.remarkets.primary.com.ar/rest/instruments/detail', params=params,
                           headers=headers)

        # Aquí está la respuesta
        response = req.text
        print(json.loads(response))

    except Exception as ex:
        print("Error durante la ejecucion del GetSegmentos {}".format(ex))


# Instrumentos: Lista de Instrumentos por Código CFI
def GetInstrumentosByCFI(XAuthToken, CFICode):
    try:

        # encabezado de solicitud http
        headers = {'X-Auth-Token': XAuthToken}

        params = {
            'CFICode': CFICode
        }

        # Agregar información de encabezado http
        req = requests.get('https://api.remarkets.primary.com.ar/rest/instruments/byCFICode', params=params,
                           headers=headers)

        # Aquí está la respuesta
        response = req.text
        print(json.loads(response))

    except Exception as ex:
        print("Error durante la ejecucion del GetSegmentos {}".format(ex))


# Instrumentos: Lista de Instrumentos por Segmentos
def GetInstrumentosBySegmento(XAuthToken, MarketSegmentID, MarketID):
    try:

        # encabezado de solicitud http
        headers = {'X-Auth-Token': XAuthToken}

        params = {
            'MarketSegmentID': MarketSegmentID,
            'MarketID': MarketID
        }

        # Agregar información de encabezado http
        req = requests.get('https://api.remarkets.primary.com.ar/rest/instruments/bySegment', params=params,
                           headers=headers)

        # Aquí está la respuesta
        response = req.text
        print(json.loads(response))

    except Exception as ex:
        print("Error durante la ejecucion del GetSegmentos {}".format(ex))


# Ordenes: Ingresar una orden
class Orden:

    def __init__(self, marketId, Symbol, Price, orderQty, ordType, side, timeInForce, account, cancelPrevious, iceberg,
                 expireDate, displayQty):
        self.marketId = marketId
        self.Symbol = Symbol
        self.Price = Price
        self.orderQty = orderQty
        self.ordType = ordType
        self.side = side
        self.timeInForce = timeInForce
        self.account = account
        self.cancelPrevious = cancelPrevious,
        self.iceberg = iceberg
        self.expireDate = expireDate
        self.displayQty = displayQty


orden = Orden(
    marketId='ROFX',
    Symbol='DLR/FEB23',
    Price='195',
    orderQty=1,
    ordType='Limit',
    side='Buy',
    timeInForce='Day',
    account='REM7609',
    cancelPrevious='',
    iceberg=0,
    expireDate='20221114',
    displayQty=''
)


def GetInsertOrden(XAuthToken, orden):
    try:

        # encabezado de solicitud http
        headers = {'X-Auth-Token': XAuthToken}

        params = {
            'marketId': orden.marketId,
            'symbol': orden.Symbol,
            'price': orden.Price,
            'orderQty': orden.orderQty,
            'ordType': orden.ordType,
            'side': orden.side,
            'timeInForce': orden.timeInForce,
            'account': orden.account
        }

        # Agregar información de encabezado http
        req = requests.get('https://api.remarkets.primary.com.ar/rest/order/newSingleOrder', params=params,
                           headers=headers)

        # Aquí está la respuesta
        response = req.text
        print(json.loads(response))

    except Exception as ex:
        print("Error durante la ejecucion del GetSegmentos {}".format(ex))


# Ordenes: Obtengo una orden por su ID
def GetEstadoByOrderId(XAuthToken, orderId):
    try:

        # encabezado de solicitud http
        headers = {'X-Auth-Token': XAuthToken}

        params = {
            'orderId': orderId
        }

        # Agregar información de encabezado http
        req = requests.get('https://api.remarkets.primary.com.ar/rest/order/byOrderId', params=params,
                           headers=headers)

        # Aquí está la respuesta
        response = req.text
        print(json.loads(response))

    except Exception as ex:
        print("Error durante la ejecucion del GetSegmentos {}".format(ex))


# Ordenes: Cancelo una orden por ID de Cliente y participante del mercado
def GetCancelarOrdenByclOrdIdAndproprietary(XAuthToken, clOrdId, proprietary):
    try:

        # encabezado de solicitud http
        headers = {'X-Auth-Token': XAuthToken}

        params = {
            'clOrdId': clOrdId,
            'proprietary': proprietary
        }

        # Agregar información de encabezado http
        req = requests.get('https://api.remarkets.primary.com.ar/rest/order/cancelById', params=params,
                           headers=headers)

        # Aquí está la respuesta
        response = req.text
        print(json.loads(response))

    except Exception as ex:
        print("Error durante la ejecucion del GetSegmentos {}".format(ex))


# Ordenes: Consulta una orden por ID de Cliente y participante del mercado
def GetConsultaOrdenByclOrdIdAndproprietary(XAuthToken, clOrdId, proprietary):
    try:

        # encabezado de solicitud http
        headers = {'X-Auth-Token': XAuthToken}

        params = {
            'clOrdId': clOrdId,
            'proprietary': proprietary
        }

        # Agregar información de encabezado http
        req = requests.get('https://api.remarkets.primary.com.ar/rest/order/id', params=params,
                           headers=headers)

        # Aquí está la respuesta
        response = req.text
        print(json.loads(response))

    except Exception as ex:
        print("Error durante la ejecucion del GetSegmentos {}".format(ex))


# Ordenes: Consulto las ordenes activas por ID de Cuenta
def GetConsultaOrdenActivas(XAuthToken, accountId):
    try:

        # encabezado de solicitud http
        headers = {'X-Auth-Token': XAuthToken}

        params = {
            'accountId': accountId
        }

        # Agregar información de encabezado http
        req = requests.get('https://api.remarkets.primary.com.ar/rest/order/actives', params=params,
                           headers=headers)

        # Aquí está la respuesta
        response = req.text
        print(json.loads(response))

    except Exception as ex:
        print("Error durante la ejecucion del GetSegmentos {}".format(ex))


# Ordenes: Consulto las ordenes que se encuentran operadas
def GetConsultaOrdenOperadas(XAuthToken, accountId):
    try:

        # encabezado de solicitud http
        headers = {'X-Auth-Token': XAuthToken}

        params = {
            'accountId': accountId
        }

        # Agregar información de encabezado http
        req = requests.get('https://api.remarkets.primary.com.ar/rest/order/filleds', params=params,
                           headers=headers)

        # Aquí está la respuesta
        response = req.text
        print(json.loads(response))

    except Exception as ex:
        print("Error durante la ejecucion del GetSegmentos {}".format(ex))


# Ordenes: Consulto todas las ordenes por ID de cuenta
def GetConsultaOrdenPorIDCuenta(XAuthToken, accountId):
    try:

        # encabezado de solicitud http
        headers = {'X-Auth-Token': XAuthToken}

        params = {
            'accountId': accountId
        }

        # Agregar información de encabezado http
        req = requests.get('https://api.remarkets.primary.com.ar/rest/order/all', params=params,
                           headers=headers)

        # Aquí está la respuesta
        response = req.text
        print(json.loads(response))

    except Exception as ex:
        print("Error durante la ejecucion del GetSegmentos {}".format(ex))


# Ordenes: Consultar todos los estados por Client Order ID
def GetConsultaAllEstadosByClientOrderID(XAuthToken, clOrdId, proprietary):
    try:

        # encabezado de solicitud http
        headers = {'X-Auth-Token': XAuthToken}

        params = {
            'clOrdId': clOrdId,
            'proprietary': proprietary
        }

        # Agregar información de encabezado http
        req = requests.get('https://api.remarkets.primary.com.ar/rest/order/allById', params=params,
                           headers=headers)

        # Aquí está la respuesta
        response = req.text
        print(json.loads(response))

    except Exception as ex:
        print("Error durante la ejecucion del GetSegmentos {}".format(ex))


# Ordenes: Estado de Orden por Execution ID
def GetEstadoByExecucionID(XAuthToken, execId):
    try:

        # encabezado de solicitud http
        headers = {'X-Auth-Token': XAuthToken}

        params = {
            'execId': execId
        }

        # Agregar información de encabezado http
        req = requests.get('https://api.remarkets.primary.com.ar/rest/order/byExecId', params=params,
                           headers=headers)

        # Aquí está la respuesta
        response = req.text
        print(json.loads(response))

    except Exception as ex:
        print("Error durante la ejecucion del GetSegmentos {}".format(ex))


# MarketData
# MarketData en tiempo real a través de REST
def GetMarketData(XAuthToken, marketId, symbol, entries, depth):
    try:

        # encabezado de solicitud http
        headers = {'X-Auth-Token': XAuthToken}

        params = {
            'marketId': marketId,
            'symbol': symbol,
            'entries': entries,
            'depth': depth
        }

        # Agregar información de encabezado http
        req = requests.get('https://api.remarkets.primary.com.ar/rest/marketdata/get', params=params,
                           headers=headers)

        # Aquí está la respuesta
        response = req.text
        print(json.loads(response))

    except Exception as ex:
        print("Error durante la ejecucion del GetSegmentos {}".format(ex))


print("===== Comienzo BOT ====")
XAuthToken = PostToken()
# GetSegmentos(XAuthToken)
GetInstrumentos(XAuthToken)
# GetInstrumentosDetalle(XAuthToken)
# GetInstrumentoDetalle(XAuthToken, 'ROFX', 'MAI.ROS/DIC22 272 C')
# GetInstrumentosByCFI(XAuthToken, 'DBXXXX')
# GetInstrumentosBySegmento(XAuthToken, 'DDF', 'ROFX')
# GetInsertOrden(XAuthToken, orden)
# GetEstadoByOrderId(XAuthToken, '406908960692914')
# GetCancelarOrdenByclOrdIdAndproprietary(XAuthToken,'406910496751807', 'PBCP')
# GetConsultaOrdenByclOrdIdAndproprietary(XAuthToken, '406910715760073', 'PBCP')
# GetConsultaOrdenActivas(XAuthToken, 'REM7609')
# GetConsultaOrdenOperadas(XAuthToken, 'REM7609')
# GetConsultaOrdenPorIDCuenta(XAuthToken, 'REM7609')
# GetConsultaAllEstadosByClientOrderID(XAuthToken, '406910715760073', 'PBCP')
# GetMarketData(XAuthToken, 'ROFX', 'MAI.ROS/DIC22 272 C', 'BI,OF,LA,OP,CL,SE,OI', 1)


#IMPORT APIROFEX