import requests
import json
from bs4 import BeautifulSoup

response = requests.get("https://mercatox.com/api/public/v1/asset")
#‘endpoint’ - Endpoint of API you are accessing,
#‘params’ - incoming request parameters (if required)
url = 'https://mercatox.com/api/public/v1/asset'
#print(assets.json())
data = response.json()

for item in data["XRB"]:
    print("item is:" + str(item))

print(data["XRB"]["taker_fee"])

#Fee of Nano / XRB
fee_mercatox = data["XRB"]["taker_fee"]