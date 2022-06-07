# Here it will only have the code and attributes that uses in Binance
from kraken import volume, Bwithdrawfee
from binance import Client
# API secret and API key
from auth import binance_api_key, binance_api_sec
Bwithdrawfee = 0.02 #https://www.binance.com/en/fee/cryptoFee

# Firstly we have the API
client = Client(binance_api_sec, binance_api_key)
api_url = "https://api.binance.com"
# Minimum for trade
Bminimum_xno = 0.024
trade_fee_XNOUSDT = float(client.get_trade_fee(symbol='XNOUSDT')[0]["takerCommission"]) * volume


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


def retBbalance_USDT():
    # If wanted to see the balance in the pair USDT
    Bbalance_USDT = client.get_asset_balance(asset='USDT')["free"]
    return Bbalance_USDT


# if bought in Binance

B_custo_total = float(Bwithdrawfee) + (volume * trade_fee_XNOUSDT)
NANO_Buy_PriceB = xno_price + trade_fee_XNOUSDT + Bwithdrawfee
NANO_QuantityB = volume/xno_price
NANO_ExitfromBinance = NANO_QuantityB - Bwithdrawfee

BinanceSell = xno_price * volume - (trade_fee_XNOUSDT * volume)
# Here we know that we will sell less than the volume bought(because of withdraw fees and taxes where we bough NANO), still we are using it
# To be more easy to do it, and so we have a calculation of fee in other function
