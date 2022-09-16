# Here it will only have the code and attributes that uses in Binance
from kraken import volume
from binance import Client
# API secret and API key
from auth import binance_api_key, binance_api_sec

Bwithdrawfee = 0.023  # https://www.binance.com/en/fee/cryptoFee

# Firstly we have the API
client = Client(binance_api_sec, binance_api_key)
api_url = "https://api.binance.com"

# Here it's the variables like taxes and so on, that is constantly changed by the exchanges:

Bminimum_xno = 0.06  # Minimum value for trade at https://www.binance.com/en/fee/cryptoFee
Bwithdrawfee = 0.03  # Withdraw fee at https://www.binance.com/en/fee/cryptoFee

# Fee
trade_fee_XNOUSDT = float(client.get_trade_fee(symbol='XNOUSDT')[0]["takerCommission"]) * volume
trade_fee_XNOBUSD = float(client.get_trade_fee(symbol='XNOBUSD')[0]["takerCommission"]) * volume

def binancebalancecoin(coin):
    balance = client.get_asset_balance(asset=coin)
    return balance


def retBaddress():
    # Deposit adress for Binance XNO
    Baddress = client.get_deposit_address(coin='XNO')
    Baddress = Baddress['address']
    return Baddress


def retminimumtrade():
    # Minimum for trade
    return Bminimum_xno


# https://www.binance.com/en/fee/cryptoFee

# Consulta preço em XNO/Binance
# For liquidity reasons, lets use the pair XNOUSDT
xno = client.get_symbol_ticker(symbol="XNOUSDT")
xno_price = float(xno["price"])
# Let´s use also the pair XNOBUSD
xnob = client.get_symbol_ticker(symbol="XNOUSDT")
xno_priceBUSD = float(xnob["price"])


def retBbalance_USDT():
    # If wanted to see the balance in the pair USDT
    Bbalance_USDT = client.get_asset_balance(asset='USDT')["free"]
    return Bbalance_USDT


def getdepositadressbinance(symbol):
    # Get the deposit address
    binanceadress = client.get_deposit_adress(coin='symbol')
    # For NANO it´s XNO
    return binanceadress


# if bought in Binance

B_custo_total = float(Bwithdrawfee) + (volume * trade_fee_XNOUSDT)
NANO_Buy_PriceB = xno_price + trade_fee_XNOUSDT + Bwithdrawfee
NANO_QuantityB = volume / xno_price
NANO_ExitfromBinance = NANO_QuantityB - Bwithdrawfee

BinanceSell = xno_price * volume - (trade_fee_XNOUSDT / 100 * volume)
# Here we know that we will sell less than the volume bought(because of withdraw fees and taxes where we bought NANO),
# still we are using it To be more easy to do it, and so we have a calculation of fee in other function
