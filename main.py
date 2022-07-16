import os
import interactions as it
from interactions import Client, Button, ButtonStyle, SelectMenu, SelectOption, ActionRow, Modal, TextInput,TextStyleType
from interactions import CommandContext as CC
from interactions import ComponentContext as CPC
import datetime

import time
import math

import logging


presence = it.PresenceActivity(name="utilities and games", type=it.PresenceActivityType.GAME)
bot = Client(token=os.getenv("TOKEN"),presence=it.ClientPresence(activities=[presence]),disable_sync=False)

@bot.event
async def on_ready():
    bot_name = bot.me.name
    print(f"Logged in as {bot_name}!")


#bot.load buggy with for-loop, so fk me ,hardcode it

bot.load("cogs.movies")
print("movies loaded")
bot.load("cogs.crypto")
print("crypto loaded")
bot.load("cogs.weather")
print("weather loaded")
bot.start()
