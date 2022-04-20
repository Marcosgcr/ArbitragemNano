from binance import Client  # , ThreadedWebsocketManager, ThreadedDepthCacheManager
from AuthK import (binance_api_key, binance_api_sec)
from AuthK import (kraken_api_sec, kraken_api_key)
import time
# import os
import requests
import urllib.parse
import hashlib
import hmac
import base64

# import json
# import websocket
# from binance.enums import *

#################################################
client = Client(binance_api_sec, binance_api_key)
#################################################
api_url = "https://api.binance.com"
kraken_api_url = "https://api.kraken.com"


#################################################

def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


# Attaches auth headers and returns results of a POST request
def kraken_request(uri_path, data, kraken_api_key, kraken_api_sec):
    headers = {}
    headers['API-Key'] = kraken_api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(uri_path, data, kraken_api_sec)
    req = requests.post((kraken_api_url + uri_path), headers=headers, data=data)
    return req


#############################################################################
# VARIAVEIS

# Consulta saldo em NANO/Kraken
resp = kraken_request('/0/private/Balance', {
    "nonce": str(int(1000 * time.time())),
}, kraken_api_key, kraken_api_sec)
jsonresponse = resp.json()
NANO_Balance = jsonresponse["result"]["NANO"]
# print(jsonresponse["result"]["NANO"])


# Consulta preço NANO/Kraken
resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=NANOUSD')
jsonresponse = resp.json()

NANO_ask = jsonresponse["result"]["NANOUSD"]["a"]
NANO_ask_price = float(NANO_ask[0])

NANO_bid = jsonresponse["result"]["NANOUSD"]["a"]
NANO_bid_price = float(NANO_bid[0])

# Fees withdraw Nano Kraken
Kminimum_nano = 0.1
Kwithdraw_fee_nano = 0.05

# Consulta preço em XNO/Binance
xno = client.get_symbol_ticker(symbol="XNOUSDT")
xno_price = float(xno["price"])

# Saldo USDT na Binance
Bbalance_USDT = client.get_asset_balance(asset='USDT')["free"]

Bvolume = float(Bbalance_USDT) / float(xno_price)

# Fee total
Btrade_fee_XNOUSDT = float(client.get_trade_fee(symbol='XNOUSDT')[0]["makerCommission"])

# Saldo USDT na Kraken
resp = kraken_request('/0/private/Balance', {
    "nonce": str(int(1000 * time.time())),
}, kraken_api_key, kraken_api_sec)
jsonresponse = resp.json()
Kbalance_USDT = 19
# Kbalance_USDT = jsonresponse["result"]["USDT"]


# Custo Total Fee Kraken (comprar e sacar da Kraken)

Kvolume = float(Kbalance_USDT) / float(NANO_bid_price)
Ktrade_fee = Kvolume * (0.22 / 100)
Kcusto_total = float(Ktrade_fee) + float(Kwithdraw_fee_nano)

# Txa total se comprar na binance
Bwithdraw_fee_xno = 0.012
# https://www.binance.com/en/fee/cryptoFee
# Custo Total Fee Binance (comprar e sacar da binance)
B_custo_total = float(Bwithdraw_fee_xno) + (Bvolume * Btrade_fee_XNOUSDT)

# Minimo para trade
Bminimum_xno = 0.024
# https://www.binance.com/en/fee/cryptoFee


# Deposito Binance
Baddress = client.get_deposit_address(coin='XNO')
# Deposito Kraken
# \resp = kraken_request('/0/private/DepositAddresses', {
#    "nonce": str(int(1000*time.time())),
#    "asset": "NANO",
#    "method": "NANO",
#     "new": False
# }, kraken_api_key, kraken_api_sec)
# jsonresponse = resp.json()
# print(resp.json())
# print(jsonresponse["result"][0]['address'])
# Kaddress = jsonresponse["result"][0]['address']
Kaddress = "nano_1kcnp5qcix7jtjx3birw86tpzhajqif9j4uk55inhpu6qbfdxwxciqnbhoes"
Ksaque = float(Kvolume) - (float(Ktrade_fee) * float(Kvolume))
Bsaque = float(Bvolume) - (float(Btrade_fee_XNOUSDT) * float(Kvolume))

if xno_price != NANO_bid_price and xno_price > 0 and NANO_bid_price > 0:
    # Se preço da Nano na Binance < preço da Nano na Kraken
    if xno_price < NANO_bid_price and \
            Bvolume > Bminimum_xno and \
            NANO_ask_price * Bsaque > B_custo_total + (Ktrade_fee * Bsaque) + (0.025 * Bvolume) and 1 == 2:
        # volume = saldo binance
        order = client.order_limit_buy(
            symbol='XNOUSDT',
            quantity=Bvolume,
            price=xno_price)
        orders = client.get_open_orders(symbol='XNOUSDT')
        print(orders)
    # print(order = client.get_order(  symbol='XNOUSDT',orderId='orderId'))
    # Adicionar passo de segurança para verificar se comprou
    # Saque abaixo
    result = client.withdraw(
        coin='NANO',
        address=Kaddress,
        amount=Bsaque,
        name='Withdraw')
    #Passo de segurança para verificar se sacou
        if

    # Se preço da Nano na Kraken < preço da Nano na Binance
    if NANO_ask_price * Ksaque < xno_price and Kvolume > Kminimum_xno and xno_price > Kcusto_total + (
            Btrade_fee * Ksaque) + (0.026 * Ksaque):
        resp = kraken_request('/0/private/AddOrder', {
            "nonce": str(int(1000 * time.time())),
            "ordertype": "limit",
            "type": "buy",
            "volume": Kvolume,
            "pair": "NANOUSDT",
            "price": NANO_ask_price
        }, kraken_api_key, kraken_api_sec)
    # Aguardar 100segundos para dar tempo para a ordem ser feita
        time.sleep(100)
    # Variavel Ksaque
    # Adicionar um passo de segurança para verificar se comprou
    resp = kraken_request('/0/private/Withdraw', {
        "nonce": str(int(1000 * time.time())),
        "asset": "NANO",
        "key": Baddress,
        "amount": Ksaque
    }, kraken_api_key, kraken_api_sec)
    resp = kraken_request('/0/private/WithdrawStatus', {
        "nonce": str(int(1000 * time.time())),
        "asset": "NANO"
    }, api_key, api_sec)
    print(resp.json())
