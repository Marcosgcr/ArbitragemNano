# Here we have only the code from Kraken API
import requests
import urllib.parse
import hashlib
import hmac
import base64
import time
from auth import kraken_api_key, kraken_api_sec

# Put here the deposit address for NANO at kraken
Kraken_deposit = "nano_1kcnp5qcix7jtjx3birw86tpzhajqif9j4uk55inhpu6qbfdxwxciqnbhoes"
kraken_api_url = "https://api.kraken.com"

# Here it is info that can be changed easily

Kminimum_nano = 0.1  # minimum that can be withdraw from Kraken
Kwithdraw_fee_nano = 0.0550648  # Withdraw fees at https://support.kraken.com/hc/pt/articles/360000767986-Taxas-e-valores
# -m%C3%ADnimos-para-retirada-de-criptomoedas
volume = 100  # Volume of USDT used in this operation in any exchange
Ktrade_fee = volume * (0.26 / 100)  # Fee #it can be automated, see the final part
pair = "NANOUSDT"
ticker_kraken = "NANO"


# Here it ends the  info that can be changed easily

def kbuyorder(pair_token, volumeof, price_order):
    if print(kraken_request('/0/private/AddOrder', {
        "nonce": str(int(1000 * time.time())),
        "ordertype": "limit",
        "type": "buy",
        "volume": volumeof,
        "pair": pair_token,
        "price": price_order,
    }, kraken_api_key, kraken_api_sec)) == 200:
        kraken_request('/0/private/AddOrder', {
            "nonce": str(int(1000 * time.time())),
            "ordertype": "limit",
            "type": "buy",
            "volume": volumeof,
            "pair": pair_token,
            "price": price_order,
        }, kraken_api_key, kraken_api_sec)


def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


# Attaches auth headers and returns results of a POST request
# noinspection PyTypeChecker
def kraken_request(uri_path: object, data: object, kraken_api_key: object, kraken_api_sec: object) -> object:
    headers = {}
    headers['API-Key'] = kraken_api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(uri_path, data, kraken_api_sec)
    # noinspection PyTypeChecker
    req = requests.post((kraken_api_url + uri_path), headers=headers, data=data)
    return req


# If we want to see the price NANO
resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=NANOUSD')
jsonresponse = resp.json()

NANO_ask = jsonresponse["result"]["NANOUSD"]["a"]
NANO_ask_price = float(NANO_ask[0])

NANO_bid = jsonresponse["result"]["NANOUSD"]["a"]
NANO_bid_price = float(NANO_bid[0])


# Nano Ask is Sell, and Nano Bid is buy

# If we want to see the balance in Nano or other coin at Kraken
def balancekraken(coin):
    resp = kraken_request('/0/private/Balance', {
        "nonce": str(int(1000 * time.time())),
    }, kraken_api_key, kraken_api_sec)
    jsonresponse = resp.json()
    Balance = jsonresponse["result"][coin]
    return Balance


# print(jsonresponse["result"]["NANO"]) -- if we withdraw the comment on this we can print the balance

# Here it is calculation the Price of Nano with all the costs including withdraw from Kraken
NANO_Buy_PriceK = NANO_bid_price + Ktrade_fee + Kwithdraw_fee_nano

# If we sell on Kraken
# here it will be used the ask price
KrakenSell = NANO_ask_price * volume - Ktrade_fee
NANO_QuantityK = volume / NANO_bid_price
NANO_ExitfromKraken = NANO_QuantityK - Kwithdraw_fee_nano

# To see what is the tax on Kraken
# resp = kraken_request('/0/private/TradeVolume', {
#    "nonce": str(int(1000 * time.time())),
#    "fee-info": True,
#    "pair": "NANOUSD"
# }, kraken_api_key, kraken_api_sec)
# jsonresponse = resp.json()
# for key, value in jsonresponse["result"].items():
#    print(key, "", value)
