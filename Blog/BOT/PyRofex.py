import pyRofex
import threading


# get_segments: gets a list of valid segments.
# get_all_instruments: gets a list of all available instruments.
# get_detailed_instruments: gets a detailed list of all available instruments.
# get_instrument_details: gets the details of a single instrument.
# get_market_data: gets market data information for an instrument.
# get_trade_history: gets a list of historic trades for an instrument.
# send_order: sends a new order to the Market.
# cancel_order: cancels an order.
# get_order_status: gets the status of the specified order.
# get_all_orders_status: gets the status of all the orders associated with an account.
# get_account_position: gets the status of the account positions.
# get_detailed_position: gets the status of detailed account asset positions by asset type.
# get_account_report: gets the summary of associated account.

class PyRofex():

    def __init__(self, Usuario, Password, Cuenta):
        self.Usuario = Usuario
        self.Password = Password
        self.Cuenta = Cuenta

    def Inicializar(self):
        # Set the the parameter for the REMARKET environment
        return pyRofex.initialize(user=Usuario, password=Password, account=Cuenta,
                                  environment=pyRofex.Environment.REMARKET)

    def GetSegments(self):
        # Gets all segments
        return pyRofex.get_segments()

    def GetAllInstruments(self):
        # Gets available instruments list
        return pyRofex.get_all_instruments()

    def GetDetailedInstruments(self):
        # Gets detailed instruments list
        return pyRofex.get_detailed_instruments()

    def GetAllOrdersStatus(self):
        # Get all order report for the configured account
        return pyRofex.get_all_orders_status()

    def GetTradeHistory(self, ticker, start_date, end_date):
        # Gets historic trades
        return pyRofex.get_trade_history(ticker=ticker, start_date=start_date, end_date=end_date)

    def SendOrder(self, ticker, size, price):
        # Sends a Limit order to the market
        return pyRofex.send_order(ticker=ticker,
                                  side=self.pyRofex.Side.BUY,
                                  size=size,
                                  price=price,
                                  order_type=self.pyRofex.OrderType.LIMIT)

    def GetOrderStatus(self, order, clientId):
        # Gets the last order status for the previous order
        return pyRofex.get_order_status(order[order][clientId])

    def CancelOrder(self, order, clientId):
        # Cancels the previous order
        return pyRofex.cancel_order(order[order][clientId])

    def GetOrderStatusCancel(self, order, clientId):
        # Checks the order status of the cancellation order
        return pyRofex.get_order_status(cancel_order[order][clientId])


# First we define the handlers that will process the messages and exceptions.
def market_data_handler(message):
    print("Market Data Message Received: {0}".format(message))


def order_report_handler(message):
    print("Order Report Message Received: {0}".format(message))


def error_handler(message):
    print("Error Message Received: {0}".format(message))


def exception_handler(e):
    print("Exception Occurred: {0}".format(e.message))


def Connect():
    # Initiate Websocket Connection
    pyRofex.init_websocket_connection(market_data_handler=market_data_handler,
                                      order_report_handler=order_report_handler,
                                      error_handler=error_handler,
                                      exception_handler=exception_handler)

    # Instruments list to subscribe
    instruments = ["ORO/MAR23"]
    # Uses the MarketDataEntry enum to define the entries we want to subscribe to
    entries = [pyRofex.MarketDataEntry.BIDS,
               pyRofex.MarketDataEntry.OFFERS,
               pyRofex.MarketDataEntry.LAST]

    # Subscribes to receive market data messages **
    pyRofex.market_data_subscription(tickers=instruments,
                                     entries=entries)

    # Subscribes to receive order report messages (default account will be used) **
    pyRofex.order_report_subscription()


Usuario = 'nnico36917609'
Password = 'epfomT3('
Cuenta = 'REM7609'

_pyRofex = PyRofex(Usuario, Password, Cuenta)
_pyRofex.Inicializar()

hilo = threading.Thread(name='init_websocket_connection',
                        target=Connect)

hilo.start()

allInstrumento = _pyRofex.GetAllInstruments()

for instrumento in allInstrumento['instruments']:
    print(instrumento)

