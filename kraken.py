# Here we have only the code from Kraken API
import requests
import urllib.parse
import hashlib
import hmac
import base64
import time
from auth import kraken_api_key, kraken_api_sec

kraken_api_url = "https://api.kraken.com"

# Here it is info that can be changed easily

Kminimum_nano = 0.1 #minimum that can be withdraw from Kraken
Kwithdraw_fee_nano = 0.05 #Withdraw fees
volume = 100  #Volume of USDT used in this operation in any exchange
Ktrade_fee = volume * (0.016 / 100) #Fee #it can be automate, see the final part
Bwithdrawfee = 0.02 #https://www.binance.com/en/fee/cryptoFee
# Here it ends the  info that can be changed easily

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


# If we want to see the price NANO
resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=NANOUSD')
jsonresponse = resp.json()

NANO_ask = jsonresponse["result"]["NANOUSD"]["a"]
NANO_ask_price = float(NANO_ask[0])


NANO_bid = jsonresponse["result"]["NANOUSD"]["a"]
NANO_bid_price = float(NANO_bid[0])

# Nano Ask is Sell, and Nano Bid is buy

# If we want to see the balance in Nano at Kraken
resp = kraken_request('/0/private/Balance', {
    "nonce": str(int(1000 * time.time())),
}, kraken_api_key, kraken_api_sec)
jsonresponse = resp.json()
NANO_Balance = jsonresponse["result"]["NANO"]
# print(jsonresponse["result"]["NANO"]) -- if we withdraw the comment on this we can print the balance

#Here it is calculation the Price of Nano with all the costs including withdraw from Kraken
NANO_Buy_PriceK = NANO_bid_price + Ktrade_fee + Kwithdraw_fee_nano
NANO_Buy_PriceKZ = NANO_bid_price  + Kwithdraw_fee_nano
#If we sell on Kraken
# here it will be used the ask price
KrakenSell= NANO_ask_price * volume - Ktrade_fee
NANO_QuantityK = volume/NANO_bid_price
NANO_ExitfromKraken = NANO_QuantityK - Kwithdraw_fee_nano

#To see what is the tax on Kraken
resp= kraken_request('/0/private/TradeVolume', {
    "nonce": str(int(1000*time.time())),
    "fee-info": True,
    "pair": "NANOUSD"
}, kraken_api_key, kraken_api_sec)
jsonresponse = resp.json()
#for key, value in jsonresponse["result"].items():
#    print(key, "", value)