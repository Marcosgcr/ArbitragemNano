![GitHub last commit](https://img.shields.io/github/last-commit/Marcosgcr/ArbitragemNano)
![GitHub followers](https://img.shields.io/github/followers/Marcosgcr?style=social)
![GitHub Repo stars](https://img.shields.io/github/stars/Marcosgcr/ArbitragemNano?style=social)
![GitHub forks](https://img.shields.io/github/forks/Marcosgcr/ArbitragemNano?style=social)



The project is well comented in the code in plain English. I am open to contribuiters for the code. Thank you. 

## What is this Project?

This is a project to use the differences in price between exchanges to buy and sell criptocurrency between them. In other words, do arbitrage. This is possible because criptocurrencys are descentralized.
In stocks and other 'regular' assets, they are all negociated in one place. For example, if you want to buy Microsoft stock, it dosn´t matter which broker do you use, because all the demand and supply of the asset are in one place.
In crypto, its different. 
Since you can withdraw and move the assets freely (as default) all crypto exchanges have supply and demand different from each other. Sometimes you can buy Bitcoin cheaper in Binance than in Kraken for example.
Using this idea, that it´s used for many years in the crypto industry so called *arbitrage. 

## Why Nano(XNO)?

This project today uses only Nano(XNO) to arbitrage. This can be used with many other crypto but i choose only Nano to simplify this process.
Also, this project have mainly financial porposes, that said it needs a crypto that has less or zero fees to move in the net and the most fast between exchanges.
This is a perfect job for Nano, cause it´s feelees (*yes, most crypto has fees to move around*) and it is fast.

More details about NANO: https://nano.org/



ArbitragemNano

Este é um projeto com o intuito de realizar arbitragem da criptomoeda NANO entre duas corretoras diferentes para no fim obter lucro.

Por ser um mercado descentralizado, cada corretora de criptomoedas possui um preço devido a oferta e demanda serem divergentes em cada sítio, isto é diferentemente da bolsa de valores de São Paulo( a B3), ou qualquer "padrão", como Nasdaq entre outras.T
odos ativos negociados no mercado secundário precisam passar pela B3. 

Assim, independendente da corretora que está operando para comprar ações seja XP ou Banco Inter ,por exemplo isto não afetará o preço do ativo, pelo fato de que todos ativos são negociados na bolsa de valores, assim não importando qual corretora usar para  adquirir ações, o preço vai ser o mesmo na corretora X ou Y no mesmo horário,data e quantidade ofertada. 
Porém, isto não é verdade em ativos descentralizados, isto é as criptomoedas. 
Assim, vem a ideia de arbitrar entre corretoras, comprar onde está barato e vender onde está mais caro.

A ideia é simples, mas é composta por muitas variáveis tais como integração API com as corretoras, taxas, volatilidade de mercado e escolha do ativo a ser arbitrato.

O ativo escolhido foi a https://nano.org/ ,NANO(XNO), ativo com transações quase que instantaneas e rede capaz de ter uma taxa nula de transferencia.
Por estar realizando um projeto com fim financeiro, é imprescendivel a velocidade e baixo custo que o ativo deve proporcionar e este é o caso com a NANO. 
Infelizmente não consigo fugir das taxas de saque,deposito e negociação das corretoras então este estão como variáveis dentro do codigo.

Usando a documentação API da Kraken: https://docs.kraken.com/rest/
Usando a documentação API de cliente da Binance: https://binance-docs.github.io/apidocs/spot/en/#change-log


Pelo coinmarketcap, verifiquei as corretoras com maior negociação da criptomoeda escolhida e que tenham uma API de preferencia com Python para eu interagir.
Escolhi a Binance e a Kraken


