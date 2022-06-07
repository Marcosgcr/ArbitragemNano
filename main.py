# Here we import the API´s exchanges from the file auth and variables needed to do the main thing
# Need to install the package python-binance here if dont has it
import time
from binancelocal import BinanceSell, NANO_Buy_PriceB, NANO_QuantityB, xno_price, trade_fee_XNOUSDT, \
    NANO_ExitfromBinance
from kraken import KrakenSell, NANO_QuantityK, NANO_ask_price, NANO_ExitfromKraken, NANO_Buy_PriceK, volume, Ktrade_fee, NANO_Buy_PriceKZ
from gemini import GeminiSell, NANO_Buy_PriceG
from auth import (kraken_api_sec, kraken_api_key, binance_api_sec, binance_api_key, gemini_api_sec, gemini_api_key)

Lucro = 0
volumeK = 100

while Lucro == 0:
    def getMenorPrecoCorretora():
        Quantity = 0

        # If the overral price in Kraken is less pricey than Binance
        if float(NANO_Buy_PriceK) < float(NANO_Buy_PriceB):
            Price = NANO_Buy_PriceK
            corretora = "KRAKEN"
        # If the overral price in Binance is less pricey than Kraken
        if float(NANO_Buy_PriceB) < float(NANO_Buy_PriceK):
            Price = NANO_Buy_PriceB
            corretora = "BINANCE"
        # If the overral price in Gemini is less pricey than Binance
        if float(NANO_Buy_PriceG) < float(NANO_Buy_PriceB):
            Price = NANO_Buy_PriceG
            corretora = "GEMINI"
        return corretora


    print("Quantidade de Nano que pode ser comprada na Kraken é {1} E preço total é {0} ".format(NANO_Buy_PriceK,
                                                                                                 NANO_QuantityK))
    print("Quantidade de Nano que pode ser comprada na Binance é {1} E preço total é {0} ".format(NANO_Buy_PriceB,
                                                                                                  NANO_QuantityB))


    def getHighSell():
        corretoraSell = 1
        if getMenorPrecoCorretora() == "KRAKEN":
            if BinanceSell > GeminiSell:
                corretoraSell = "BINANCE"
            if GeminiSell > BinanceSell:
                corretoraSell = "GEMINI"

        if getMenorPrecoCorretora() == "BINANCE":
            if KrakenSell > GeminiSell:
                corretoraSell = "KRAKEN"
            if GeminiSell > KrakenSell:
                corretoraSell = "GEMINI"

        if getMenorPrecoCorretora() == "GEMINI":
            if BinanceSell > KrakenSell:
                corretoraSell = "BINANCE"
            if KrakenSell > BinanceSell:
                corretoraSell = "KRAKEN"

        return corretoraSell

    if getMenorPrecoCorretora() == "KRAKEN" and getHighSell() == "BINANCE":
        print("Analisando compra na Kraken e venda na Binance...")
        if xno_price * NANO_ExitfromKraken > NANO_Buy_PriceKZ * volume :
            #xno_price * NANO_ExitfromKraken - trade_fee_XNOUSDT > NANO_Buy_PriceK * volume * 1.025
            print("Lucro nesta operação!")
            ativacao = 1
            #Ativar compra na Kraken e venda na Binance
            break
        else:
            print("Não haveria lucro nesta operação, pesquisando novamente")

        if getMenorPrecoCorretora() == "KRAKEN" and getHighSell() == "GEMINI":
            # priceongemini * NANO_ExitfromKraken
            pass
        if getMenorPrecoCorretora() == "BINANCE" and getHighSell() == "KRAKEN":
            print("Analisando compra na Binance e venda na Kraken")
            if xno_price * NANO_ExitfromKraken - trade_fee_XNOUSDT > NANO_Buy_PriceK * volume * 1.025:
                print("Lucro nesta operação!,Sendo preço de venda {} e preço de compra {}".format(NANO_ask_price * NANO_ExitfromBinance - Ktrade_fee,NANO_Buy_PriceK * volume))
                ativacao = 1

        if getMenorPrecoCorretora() == "BINANCE" and getHighSell() == "GEMINI":
            pass
        if getMenorPrecoCorretora() == "GEMINI" and getHighSell() == "BINANCE":
            pass
        if getMenorPrecoCorretora() == "GEMINI" and getHighSell() == "KRAKEN":
            pass


    #  if getHighSell() == "BINANCE":
    #      print("Ira vender na Binance")
    if getHighSell() == "GEMINI":
        print("Ira vender na Gemini")
    if getHighSell() == "KRAKEN":
        print("Ira vender na Kraken")

    #Venda na Kraken > Compra na Binance + 20%
    if NANO_ask_price * NANO_ExitfromBinance - Ktrade_fee > NANO_Buy_PriceB * volume * 1.21:
        print("Profit in this operation!")
        Lucro = 1
        print("Buy would be {}".format(NANO_Buy_PriceB * volume *1.21))
        print("Sell would be {0} and volume {1}".format(NANO_ask_price * NANO_ExitfromBinance - Ktrade_fee,
                                                         volume))
        break
    if NANO_ask_price * NANO_ExitfromBinance - trade_fee_XNOUSDT > NANO_Buy_PriceB * volume :
        print("Would had profit in this operation!")
        Lucro = 1
        print("Buy cost would be  {}".format(NANO_Buy_PriceB * volume))
        print("Sell would be {0} and volume {1}".format(NANO_ask_price * NANO_ExitfromBinance - trade_fee_XNOUSDT,
                                                         volume))
        break
    time.sleep(2)
    volumeK = volumeK + 10
    print("Searching for arbitrage opportunity..")
    print("VolumeK actual is", volumeK)
