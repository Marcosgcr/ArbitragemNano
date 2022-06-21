# Here we import the API´s exchanges from the file auth and most of the variables from other files
import time
from binancelocal import *
from kraken import *
from binance.client import *
from auth import *

# How much profit do you need 1.00 = 0 profit, if it is 1.20 that´s 20% profit. If the arbitrage isn't 20% of profit,
# the automated process won't do it.
profit = 1.10  # here it's almost the % of the profit
realprofit = xno_price * NANO_ExitfromKraken - trade_fee_XNOUSDT - NANO_Buy_PriceK * volume * profit  # Here it is the /
# value of the profit
# Here is a function that sees where is the most bargain place to buy
def getmenorprecocorretora():
    Quantity = 0

    # If the overral price in Kraken is less pricey than Binance
    if float(NANO_Buy_PriceK) < float(NANO_Buy_PriceB):
        Price = NANO_Buy_PriceB
        corretora = "KRAKEN"
        print("The cheapest place to buy is at Kraken")
    # If the overral price in Binance is less pricey than Kraken
    if float(NANO_Buy_PriceB) < float(NANO_Buy_PriceK):
        Price = NANO_Buy_PriceB
        corretora = "BINANCE"
        print("The cheapest place to buy is at BINANCE")
    return corretora


# Here is a function that sees where is the most pricey place to sell
def gethighsell():
    corretoraSell = 1
    if KrakenSell > BinanceSell and getmenorprecocorretora() != "KRAKEN":
        # If the most expensive place to sell is KRAKEN
        corretoraSell = "KRAKEN"
    if BinanceSell > KrakenSell and getmenorprecocorretora() != "BINANCE":
        # If the most expensive place to sell is BINANCE
        corretoraSell = "BINANCE"
    return corretoraSell


# Here is the function that calculates if it has any profit the arbitrage and do the action
def IfProfit():
    ativacao = 0
    if getmenorprecocorretora() == "KRAKEN" and gethighsell() == "BINANCE":
        # If the least price to buy is on KRAKEN and the most expensive place to sell is BINANCE then
        # buys at KRAKEN and sells at BINANCE
        if xno_price * NANO_ExitfromKraken - trade_fee_XNOUSDT > NANO_Buy_PriceK * volume * profit:
            # Here it´s the sell on Binance with all the costs > All the buy costs at KRAKEN and * volume * profit
            print("Lucro nesta operação! Iniciando compra na KRAKEN e venda na BINANCE")
            # Before doing anything else, let´s see how much balance we have of NANO
            before = balancekraken("NANO")
            # Also do the same for BINANCE, we will need it later
            Bbefore = binancebalancecoin("XNO")
            # Before putting the order, there is the need to know what the volume of NANO will be
            volumeN = volume / NANO_ask_price
            # Here it´s called the function from the file Kraken to put a buy order
            kraken_request('/0/private/AddOrder', {
                "nonce": str(int(1000 * time.time())),
                "ordertype": "limit",
                "type": "buy",
                "volume": volumeN,
                "pair": "NANOUSDT",
                "price": NANO_ask_price,
            }, kraken_api_key, kraken_api_sec)
            if kraken_request.json == 200:
                # keep it going, the order was successful
                # Let´s see if we have the balance
                balancekraken(ticker_kraken)
                if before < balancekraken(ticker_kraken):
                    # That means that the buy was done
                    # Let´s send the coin for BINANCE
                    kraken_request('/0/private/Withdraw', {
                        "nonce": str(int(1000 * time.time())),
                        "asset": ticker_kraken,
                        "key": "Nano_Binance",
                        "amount": volumeN - trade_fee_XNOUSDT
                    }, kraken_api_key, kraken_api_sec)
                    # ok, the coin was sent
                    time.sleep(4)  # We will wait a bit
                    # Let´s see if the coin arrived at BINANCE
                    # We will use the balance of BINANCE earlier
                    if Bbefore < binancebalancecoin("NANO"):
                        # If yes, the coin arrived
                        # Room to improve?
                        # Now, do the sell order on BINANCE
                        client.order_limit_sell(
                            symbol="NANOUSDT",
                            quantity=NANO_ExitfromKraken,
                            price=xno_price)
                        time.sleep(10)  # Wait a bit
                        # Time for see if it sold
                        # Let´s use the balance again
                        if Bbefore > binancebalancecoin("NANO"):
                            # Yes, it sold
                            print("Operação bem sucedida")
                            # Calcular o lucro
                            print(f"O lucro foi de: {realprofit} usdt")
                        else:
                            while Bbefore <= binancebalancecoin("NANO"):
                                time.sleep(5)
                            if Bbefore > binancebalancecoin("NANO"):
                                # Yes, it sold
                                print("Operação bem sucedida")
                                # Calcular o lucro
                                print(f"O lucro provavelmente foi de: {realprofit} usdt")
                    else:
                        while Bbefore < binancebalancecoin("NANO"):
                            time.sleep(10)
                            errochegadaabinance = 1 + errochegadaabinance
                            print("Nano não chegou a Binance ainda,quantidade de {} segundos".format(
                                errochegadaabinance * 10))
                        if Bbefore < binancebalancecoin("NANO"):
                            # That means that the coin arrived
                            # Let´s put an order to sell it
                            client.order_limit_sell(
                                symbol="NANOUSDT",
                                quantity=NANO_ExitfromKraken,
                                price=xno_price)
                        else:
                            pass  # To be continued
                else:  # That means that the buy wasn't done for some reason
                    while before < balancekraken(ticker_kraken):
                        time.sleep(10)
                    if before < balancekraken(ticker_kraken):  # That means that the buy was done
                        # Let´s send the coin for BINANCE
                        kraken_request('/0/private/Withdraw', {
                            "nonce": str(int(1000 * time.time())),
                            "asset": ticker_kraken,
                            "key": "Nano_Binance",
                            "amount": volumeN - trade_fee_XNOUSDT
                        }, kraken_api_key, kraken_api_sec)

            else:  # The buy order returned something else than 200, that means it happened something wrong, lets do again
                return
            # Here it will confirm if the bought went in success or not
            time.sleep(4)

    if getmenorprecocorretora() == "BINANCE" and gethighsell() == "KRAKEN":
        if NANO_ask_price * NANO_ExitfromBinance - Ktrade_fee > NANO_Buy_PriceB * volume:
            print("Lucro nesta operação!Iniciando compra na BINANCE e venda na KRAKEN")
            # Iniciar compra BINANCE
            # CONFIRMAR QUE COMPROU BINANCE
            # PEDIR ENDEREÇO DEPOSITO KRAKEN
            # ENVIAR KRAKEN
            # VERIFICAR SE RECEBEU KRAKEN
            # VENDER KRAKEN
            # VERIFICAR LUCRO
            ativacao = 1


if gethighsell() == "BINANCE":
    print("Ira vender na Binance")
if gethighsell() == "KRAKEN":
    print("Ira vender na Kraken")
# print("Sell is {}".format(NANO_ask_price * NANO_ExitfromBinance - trade_fee_XNOUSDT))
# print(NANO_Buy_PriceB * volume)
while NANO_ask_price * NANO_ExitfromBinance - Ktrade_fee != NANO_Buy_PriceB * volume:
    print(f"O lucro seria de {realprofit}")
    if NANO_ask_price * NANO_ExitfromBinance - Ktrade_fee > NANO_Buy_PriceB * volume * 1.2:
        print("Lucro nesta operação! ky")
        print("Compra seria {} na Binance".format(NANO_Buy_PriceB * volume))
        print("Venda seria {0} e volume sendo {1} na Kraken".format(
            NANO_ask_price * NANO_ExitfromBinance - trade_fee_XNOUSDT, volume))
        break
    if NANO_ask_price * NANO_ExitfromBinance - Ktrade_fee > NANO_Buy_PriceB * volume * 1.2:
        print("Lucro nesta operação! uy")
        print("Compra seria {}".format(NANO_Buy_PriceB * volume))
        print("Sell seria {0} e volume sendo {1}".format(NANO_ask_price * NANO_ExitfromBinance - trade_fee_XNOUSDT,
                                                         volume))
        break
