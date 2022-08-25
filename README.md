![GitHub last commit](https://img.shields.io/github/last-commit/Marcosgcr/ArbitragemNano)
![GitHub followers](https://img.shields.io/github/followers/Marcosgcr?style=social)
![GitHub Repo stars](https://img.shields.io/github/stars/Marcosgcr/ArbitragemNano?style=social)
![GitHub forks](https://img.shields.io/github/forks/Marcosgcr/ArbitragemNano?style=social)


## What is this Project?

This is a project to use the differences in price between exchanges to buy and sell criptocurrency between them. 
In other words, do arbitrage. This is possible because criptocurrencys are descentralized.

In stocks and other 'regular' assets, they are all negociated in one place. For example, if you want to buy Microsoft stock, it dosn´t matter which broker do you use, because all the demand and supply of the asset are in one place.
In crypto, its different. 
Since you can withdraw and move the assets freely (as default) all crypto exchanges have supply and demand different from each other.
Sometimes you can buy Bitcoin cheaper in Binance than in Kraken for example.

Using this idea, I created this project to do what is callled *arbitrage*. 
The idea here is to buy Nano(XNO) where it is more cheap and sell where it is more expensive.

## Why Nano(XNO)?

This project today uses only Nano(XNO) to arbitrage. 

This can be used with many other crypto but I choose only Nano to simplify this process. 

Also, this project have mainly financial porposes, that said it needs a crypto that has less or zero fees to move in the net and the fastest between exchanges.

This is a perfect job for Nano, cause it´s feelees (*yes, most crypto has fees to move around*) and it is fast. 

More details about NANO: https://nano.org/

## Can I use?

Yes, you can use, do a fork and modify the project, but read the license of the project here [LICENSE](LICENSE) before doing anything.

Beware of the code, since the code does mess with exchanges balances such as Binance, such as  put orders to buy,sell and withdraw, you need to review the code, since using it may have chances to go on loss and profit(that is the goal here).

Also, you do have to add API´s keys and secrets, and  edit current deposit/withdraw addresses
## Liability

*I am not in any way responsible for any loss that you may have using this code or either a modified version of this project*

## What i need to know to use?/ What is been used in this program?

For use or modify this code you *must* have understanding of Python , the library [binance-local](https://python-binance.readthedocs.io/en/latest/) and [Kraken API](https://docs.kraken.com/rest/), and basic undestanding of how Kraken and Binance exchanges works.

You can see the dependencies of the project [here](https://github.com/Marcosgcr/ArbitragemNano/blob/main/requirements.txt)
Before of downloading the requirement library I suggest you read the docs about it or the [github repository](https://github.com/sammchardy/python-binance).


## The program is finished/ is tested?

Always the program can have more features, like for example more coins to arbitrage and adding more exchanges to do the arbitrage.
To this day I have tested but I did not had an sucessfull arbitrage yet.
Because the program didn´t found an profit opportunity between Kraken and Binance. This  will only be a matter of time, cause the price discrepency between those happen from time to time.

*You can test it yourself, give it a try*


## How can I help?

There is many ways that you can help me.
Helping the advancing of the code on this project or helping me financially or even using it and reporting suggestion or apearings flaws.


