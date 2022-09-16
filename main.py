# Here we import the API´s exchanges from the file auth and most of the variables from other files
import time

from binancelocal import *
from kraken import *
# Here we import the library binance.client
from binance.client import *
# Here it is imported the API´s from the exchanges used
from auth import *
volume = 10
# How much profit do you need 1.00 = 0 profit, if it is 1.20 that´s 20% profit. If the arbitrage isn't 20% of profit,
# the automated process won't do it.
profit = 1.3


# Here is a function that sees where is the most bargain place to buy
def getmenorprecocorretora():
    time.sleep(1)
    Quantity = 0
    corretora = "none"
    if xno_priceBUSD < xno_price:
        NANO_Buy_PriceB = xno_priceBUSD + trade_fee_XNOBUSD + Bwithdrawfee
    else:
        NANO_Buy_PriceB = xno_price + trade_fee_XNOUSDT + Bwithdrawfee
    # If the overall price in Kraken is less pricey than Binance
    if float(NANO_Buy_PriceK) < float(NANO_Buy_PriceB):
        Price = NANO_Buy_PriceB
        corretora = "KRAKEN"
        # print("The cheapest place to buy is at Kraken")
    # If the overall price in Binance is less pricey than Kraken
    if float(NANO_Buy_PriceB) < float(NANO_Buy_PriceK):
        Price = NANO_Buy_PriceB
        corretora = "BINANCE"
        # print("The cheapest place to buy is at BINANCE")
    return corretora


def buybinancesellkraken():
    print(f"Starting the action of buy at binance and sell at Kraken")
    # First let´s see how much XNO we have in the account
    NanoBalance = client.get_asset_balance(asset='XNO')['free']
    # Putting an order to buy XNO
    print(f"The quantity of Nano is {NanoBalance}")
    if xno_priceBUSD < xno_price and binancebalancecoin('BUSD')['free'] >= volume:
        x = round(volume/xno_priceBUSD,2)
        order = client.order_limit_buy(
            symbol='XNOBUSD',
            quantity=x,
            price=xno_priceBUSD)
    else:
        x = round(volume/xno_price,2)
        order = client.order_limit_buy(
            symbol='XNOUSDT',
            quantity=x,
            price=xno_price)
    # wait a bit
    time.sleep(1)
    # See if bought
    print("Mandou a ordem!")
    while NanoBalance >= client.get_asset_balance(asset='XNO')['free']:
        time.sleep(5)
    if NanoBalance < client.get_asset_balance(asset='XNO')['free']:
        print("Buy at Binance successful")
        # Yes, we have successfully bought
        # Let´s calculate the volume of XNO in Kraken
        krakenbalancebefore = binancebalancecoin("XNO")["free"]
        print("DEBUG-Krakenbalancebefore = balancekraken(NANO)")
        # Now, let´s send XNO to Kraken,
        # Kraken address = address for NANO in Kraken file
        # client.withdraw(
        #    coin='XNO',
        #    address=Kraken_deposit,
        #    amount=volume)
        from binance.exceptions import BinanceAPIException
        try:
            # name parameter will be set to the asset value by the client if not passed
            result = client.withdraw(
                coin='XNO',
                address=Kraken_deposit,
                amount=volume)
        except BinanceAPIException as e:
            print(e)
        else:
            print("Success")
        print("DEBUG-Enviado ordem de saque para Kraken")
        # Let´s calculate how much XNO will arrive at Kraken
        arriveatkraken = volume - trade_fee_XNOUSDT - Bwithdrawfee
        # Let´s wait for when NANO arrives at Kraken
        while krakenbalancebefore == balancekraken("NANO"):
            time.sleep(2)
            if krakenbalancebefore < balancekraken("NANO"):
                kraken_request('/0/private/AddOrder', {
                    "nonce": str(int(1000 * time.time())),
                    "ordertype": "market",
                    "type": "sell",
                    "volume": arriveatkraken,
                    "pair": "NANOUSDT",
                }, kraken_api_key, kraken_api_sec)
            while binancebalancecoin("NANO") >= krakenbalancebefore:
                time.sleep(5)
                print("Nano was sent to Kraken, yet did not  sold")
            if binancebalancecoin("NANO") < krakenbalancebefore:
                print("Operation successful")


def sellatkraken():
    arriveatkraken = volume - trade_fee_XNOUSDT - Bwithdrawfee
    print("Starting selling at Kraken")


# Here is a function that sees where is the most pricey place to sell
def gethighsell():
    corretoraSell = "none"
    time.sleep(2)
    # print(f"Nano price is {NANO_bid_price} at Kraken")
    # print(f"XNO PRICE IS {xno_price} at binance")
    if KrakenSell < BinanceSell and getmenorprecocorretora() != "KRAKEN":
        # KrakenSell and BinanceSell greater whose place we will get less coin
        # If the most expensive place to sell is KRAKEN
        corretoraSell = "KRAKEN"
        # print("The expensive place to sell is at Kraken")

    if BinanceSell < KrakenSell and getmenorprecocorretora() != "BINANCE":
        # If the most expensive place to sell is BINANCE
        corretoraSell = "BINANCE"
        # print("The expensive place to sell is at Binance")

        # We can´t buy and sell at the same place

        # Here we will see, what has less FEES
        # https://www.binance.com/en/fee/cryptoFee
        # 0.023(withdraw fee) and 0.10% -> Binance
        # 0.0550648(withdraw fee) and 0.26% -> Kraken
    return corretoraSell


# Here is the function that calculates if it has any profit the arbitrage and do the action
def ifprofit():
    a = 0
    while a == 0:
        time.sleep(10)
        getmenorprecocorretora()
        gethighsell()
        print("Searching for arbitrage opportunity with profit...")
        # We don´t need here to wait because the two function under already have time sleep
        if getmenorprecocorretora() == "KRAKEN" and gethighsell() == "BINANCE":
            print(f"Buy at Kraken")
            print(f"Sell at Binance")
            print(f"Buying price is {(NANO_Buy_PriceK * volume)}")
            print(f"Selling price is {xno_price * (NANO_ExitfromKraken - trade_fee_XNOUSDT)}")
            print(f"Profit is {xno_price * (NANO_ExitfromKraken - trade_fee_XNOUSDT) - (NANO_Buy_PriceK * volume)} ")
            if xno_price * (NANO_ExitfromKraken - trade_fee_XNOUSDT) > (NANO_Buy_PriceK * volume) * profit:
                a = 1
                print(f"It will buy from Kraken, send to Binance and sell it there")
                buykrakensellbinance()

        if getmenorprecocorretora() == "BINANCE" and gethighsell() == "KRAKEN":
            print("Buy at Binance")
            print("Sell at Kraken")
            print(f"Selling price is {NANO_bid_price * (NANO_ExitfromBinance - Ktrade_fee)}")
            print(f"Buying price is {xno_price * volume + trade_fee_XNOUSDT}")
            print(
                f"Profit is {NANO_bid_price * (NANO_ExitfromBinance - Ktrade_fee) - (xno_price * volume + trade_fee_XNOUSDT)}")
            if NANO_bid_price * (NANO_ExitfromBinance - Ktrade_fee) > (xno_price * volume + trade_fee_XNOUSDT) * profit or NANO_bid_price * (NANO_ExitfromBinance - Ktrade_fee) > (xno_priceBUSD * volume + trade_fee_XNOBUSD) * profit:
                a = 1
                print(f"It will buy from Binance, send to Kraken and sell it there")

                buybinancesellkraken()

    # Put here other exchanges


def fromkrakentobinance(volumeN, trade_fee_XNOUSDT, ticker_kraken):
    time.sleep(10)
    kraken_request('/0/private/Withdraw', {
        "nonce": str(int(1000 * time.time())),
        "asset": ticker_kraken,
        "key": "Nano_Binance",
        "amount": volumeN - trade_fee_XNOUSDT
    }, kraken_api_key, kraken_api_sec)


def buykrakensellbinance():
    print("Beginning the function buykrakensellbinance")
    # Here is the function that buy at Kraken
    print("Iniciando compra na KRAKEN e venda na BINANCE")
    # Before doing anything else, let´s see how much balance we have of NANO
    Kbefore = balancekraken("NANO")
    # Also do the same for BINANCE. we will need it later
    Bbefore = binancebalancecoin("XNO")
    # Before putting the order, there is the need to know what the volume of NANO will be
    volumeN = volume / NANO_ask_price
    # Here we call the function that does the buy order in Kraken
    kbuyorder(Kbefore, volumeN, NANO_ask_price)
    # Let´s send the coin for Binance
    fromkrakentobinance(volumeN, trade_fee_XNOUSDT, ticker_kraken)
    # Let´s wait a bit
    time.sleep(1)
    # Let´s see if the coin arrived at BINANCE
    # We will use the balance of BINANCE earlier and after that sell NANO at Binance with the function sellatbinance
    sellatbinance(Bbefore)


def sellatbinance(b_balance_before):
    if b_balance_before < binancebalancecoin("NANO"):
        time.sleep(10)
        client.order_limit_sell(
            symbol="NANOUSDT",
            quantity=NANO_ExitfromKraken,
            price=xno_price)
        if b_balance_before > binancebalancecoin("NANO"):
            # Yes, it sold
            print("Operation successful")
            # Calculate the profit
            print(f"The profit was {realprofit} usdt")
        else:
            while b_balance_before <= binancebalancecoin("NANO"):
                time.sleep(15)
                print(f"Nano was sent to binance, yet didn't sold, refreshing in the next 15 seconds.")
            if b_balance_before > binancebalancecoin("NANO"):
                # Yes, it sold
                print("Operation was successful")
                # Calculate the profit
                print(f"The profit was {realprofit} usdt")


### Above all the functions needed for the code ###

## Start of the Code #

## Print hi
print(f"Hello,Starting program...")
ifprofit()


# This function uses 2 functions to get the cheapest place to buy and the pricey place to sell
# Later, it calls buybinancesellkraken() or buykrakensellbinance() function


## End of the code
# Here is the function that calls everything for now
def All():
    print("INICIANDO DEF ALL")
    ativacao = 0
    if getmenorprecocorretora() == "KRAKEN" and gethighsell() == "BINANCE" and ativacao == 1:
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
            if print(kraken_request('/0/private/AddOrder', {
                "nonce": str(int(1000 * time.time())),
                "ordertype": "limit",
                "type": "buy",
                "volume": volumeN,
                "pair": "NANOUSDT",
                "price": NANO_ask_price,
            }, kraken_api_key, kraken_api_sec)) == 200:
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
                        time.sleep(5)  # Wait a bit
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
                            errochegadaabinance = 0
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

            #   if getmenorprecocorretora() == "BINANCE" and gethighsell() == "KRAKEN":
            #       if NANO_ask_price * NANO_ExitfromBinance - Ktrade_fee > NANO_Buy_PriceB * volume:
            #           print("Lucro nesta operação!Iniciando compra na BINANCE e venda na KRAKEN")
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
    time.sleep(10)
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
