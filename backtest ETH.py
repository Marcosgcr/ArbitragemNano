# -*- coding: utf-8 -*-
"""
Created on Sun May 15 11:48:05 2022

Backtest ETH
- Comprar $10 quando cai
- Vender $10 quando sobe
- Aporte inicial de 100 dólares


@author: apoco
"""

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#carregando dados
#carregando dados
ETHUSD = pd.read_csv("E:/Professional/Documents\Disciplinas - POLI2020.1/LPAA/Codigos/Mercado Financeiro/ETH.csv")
BTCUSD = pd.read_csv("E:/Professional/Documents\Disciplinas - POLI2020.1/LPAA/Codigos/Mercado Financeiro/BTC.csv")
SP500 = pd.read_csv("E:/Professional/Documents\Disciplinas - POLI2020.1/LPAA/Codigos/Mercado Financeiro/SP500.csv")
NASDAQ = pd.read_csv("E:/Professional/Documents\Disciplinas - POLI2020.1/LPAA/Codigos/Mercado Financeiro/NASDAQ.csv")


DATA_ETH = ETHUSD.Data
DATA_CRYPTO = DATA_ETH
DATA_SP = SP500.Data

DATA_CRYPTO = DATA_CRYPTO.astype(str)



ETHUSD_DATA = ETHUSD.drop(["Data","Vol."], axis="columns")
ETHUSD_DATA = ETHUSD_DATA.stack().str.replace('.','').unstack()
ETHUSD_DATA = ETHUSD_DATA.stack().str.replace(',','.').unstack()
ETHUSD_DATA["Var%"] = ETHUSD_DATA["Var%"].str.replace("%","")
ETHUSD_DATA = ETHUSD_DATA.astype(float)
ETHUSD_FINAL = pd.concat([DATA_CRYPTO, ETHUSD_DATA],axis=1)


ETHUSD_FINAL = ETHUSD_FINAL.reset_index()
ETHUSD_FINAL.drop(columns=['index'],inplace = True)

ETH_close = ETHUSD_FINAL['Último']

ETH_close.head()


rets = pd.DataFrame(ETH_close.pct_change().iloc[1:])

wea_index = 1 * (rets+1).cumprod()

aporte_ini = 100
aporte = 10
count_aporte_plus = 0
count_aporte_minus = 0
taxa_binance = 0.075/100
taxa_br = 0.5/100
taxa = taxa_br*aporte #taxa da binance
pl = []

#com taxa da binance

for i in range(len(ETH_close)-1):
    if rets['Último'].iloc[i]>0:
        aporte_ini = (aporte_ini*(1+rets['Último'].iloc[i]))-aporte-taxa
        pl.append(aporte_ini)
        count_aporte_minus = count_aporte_minus+1
    if rets['Último'].iloc[i]<0:
        aporte_ini = (aporte_ini*(1+rets['Último'].iloc[i]))+aporte-taxa
        pl.append(aporte_ini)
        count_aporte_plus = count_aporte_plus+1
    if rets['Último'].iloc[i]==0:
        aporte_ini = (aporte_ini*(1+rets['Último'].iloc[i]))
        pl.append(aporte_ini)
        
result_aportes = 100 +((count_aporte_plus - count_aporte_minus)*10)

# wea_index.plot()


#picos

# Encontrando Picos
picos = wea_index.cummax()
picos_SHBL = pd.DataFrame(pl).cummax()

picos.plot()

#drawdowns

# Formula do drawdown
drawdown = (wea_index - picos) / picos
drawdown_SHBL = (pd.DataFrame(pl) - picos_SHBL) / picos_SHBL
drawdown.plot()
drawdown_SHBL.plot()

# Maximum Drawdown
max_ddw = drawdown.min()
max_ddw_SHBL = drawdown_SHBL.min() 

# Em Porcentagem
max_ddw * -100

# Adicionar o Wealth Index e os Picos no DF
rets['Wealth Index'] = wea_index
rets["Picos"] = picos
rets['Drawdowns'] = drawdown*100
rets['SHBL Backtest'] = pl/pl[0]


font_size = 15

fig,axes = plt.subplots(2,1, sharex= True, sharey=False)

plt.suptitle('Wealth index (para 1$)', fontsize = 20, va='top',y=0.95)


rets['Wealth Index'].plot(ax=axes[0], label = 'Retorno Acumulado ETH', legend = 'Retorno Acumulado ETH'  )
rets['SHBL Backtest'].plot(ax=axes[0], label = 'SHBL Backtest + taxas', legend = 'SHBL Backtest + taxas'  )

axes[0].set_ylabel('Riqueza Acumulada (em $)',labelpad = 15, fontsize=font_size)
axes[0].axhline(y=rets['Wealth Index'].iloc[-1], linestyle= ':',color = 'k')
axes[0].axhline(y=rets['SHBL Backtest'].iloc[-1], linestyle= ':',color = 'r')

rets['Drawdowns'].plot(ax=axes[1],label = 'Drawdown',color = 'r',legend = 'Drawdown')
axes[1].axhline(y=rets['Drawdowns'].iloc[-1], linestyle= ':',color='k')
axes[1].set_ylabel('Percentual de queda (em %)',fontsize=font_size)
axes[1].set_xlabel('Dias',labelpad = 14,fontsize=font_size)