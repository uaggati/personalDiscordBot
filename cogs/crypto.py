import interactions 
import interactions as it
from interactions import Client
from interactions import CommandContext as CC
from interactions import ComponentContext as CPC
import requests
import cryptocompare


class Money(interactions.Extension):
    """get crypto coins' trading prices"""
    def __init__(self,client:Client):
        self.btc_price = cryptocompare.get_price('BTC', currency= 'USD', full = False)['BTC']['USD']
        self.eth_price = cryptocompare.get_price('ETH', currency= 'USD', full = False)['ETH']['USD']
        self.ltc_price = cryptocompare.get_price('LTC', currency= 'USD', full = False)['LTC']['USD']
        self.tnd_price = cryptocompare.get_price('TND', currency= 'USD', full = False)['TND']['USD']
        self.tnd_to_euro = cryptocompare.get_price('TND', currency= 'EUR', full = False)['TND']['EUR']
        self.trading = {"btc_to_usd":[self.btc_price,"BTC","USD"],
                        "eth_to_usd":[self.eth_price,"ETH","USD"],
                        "ltc_to_usd":[self.ltc_price,"LTC","USD"],
                        "tnd_to_usd":[self.tnd_price,"TND","USD"],
                        "tnd_to_euro":[self.tnd_to_euro,"TND","EUR"]
                        }



    @interactions.extension_command(
        name="currency",
        description="get trading's price of given coin in usd/euro",
        options=[
            it.Option(
                name="coin",
                description="the chosen coin to look up",
                required=True,
                type=it.OptionType.STRING,
                choices=[
                        it.Choice(name="btc_to_usd",value="btc_to_usd"),
                        it.Choice(name="eth_to_usd",value="eth_to_usd"),
                        it.Choice(name="ltc_to_usd",value="ltc_to_usd"),
                        it.Choice(name="tnd_to_usd",value="tnd_to_usd"),
                        it.Choice(name="tnd_to_euro",value="tnd_to_euro")
                        ]
                     )
                ]
            )
    async def currency(self,ctx:CC,coin:str):
        await ctx.defer()
        trading_info = self.trading[coin]
        await ctx.send(f"1 {trading_info[1]} = {trading_info[0]} {trading_info[2]}")








def setup(client : Client):
    Money(client)
