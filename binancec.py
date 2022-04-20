
from binance.client import Client
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from datetime import datetime

#Connect with your API key
key = 'yourAPIKey'
secret = 'yoursecretKey'

client = Client(api_key = key, api_secret = secret)

#Get data
data = client.get_historical_klines('SUSHIUSDT',interval = '1h',start_str = '20d')

#Data cleaning
df = pd.DataFrame(data, columns=['date','open', 'high', 'low', 'close', 'volume','close_time', 'qav', 'num_trades',
                  'taker_base_vol', 'taker_quote_vol', 'ignore'])

i = 0
Date=[]
while(i<len(data)):
    Date.append(datetime.fromtimestamp(data[i][0]/1000).strftime('%Y-%m-%d %H:%M:%S'))
    i+=1
df['Date'] = Date
df.set_index('Date', inplace = True)

data = df

#Data visualisation
data['MA5'] = data['close'].ewm(span=10,adjust=False).mean()
data['MA20'] = data['close'].rolling(20).mean()

#declare figure
fig = go.Figure()

#Candlestick
fig.add_trace(go.Candlestick(x=data.index,
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'], name = 'market data'))

#Trading indicator
fig.add_trace(go.Scatter(x=data.index, y= data['MA20'],line=dict(color='blue', width=1.5), name = 'Long Term MA'))
fig.add_trace(go.Scatter(x=data.index, y= data['MA5'],line=dict(color='orange', width=1.5), name = 'Short Term MA'))

#Show
fig.show()

#Consulta preço em XNO/Binance

xno_price = client.get_symbol_ticker(symbol="XNOUSDT")
# print parcial output
print(xno_price["price"])