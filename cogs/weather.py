import interactions 
import interactions as it
from interactions import Client
from interactions import CommandContext as CC
from interactions import ComponentContext as CPC
import requests
import json
import os

class WeatherWatcher(interactions.Extension):
    """get weather info of given city if exist"""
    def __init__(self,client : Client) -> None:
        self.forensics = []
        self.current_temperature = ""
        self.current_pressure = ""
        self.current_humidity = ""
        self.api_key = os.getenv("WEATHER_KEY") #api key from OpenWeatherMap
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        self.complete_url = self.base_url + "appid=" + self.api_key + "&q=" 
        
    def get_weather(self,city_name:str):
        response = requests.get(self.complete_url+city_name) 
        weather_data = response.json() 
        if weather_data["cod"] != "404": 
            weather_main = weather_data["main"] 
            self.current_temperature = format((weather_main["temp"] - 273.15),'.1f')
            self.forensics.append(self.current_temperature)
            self.current_pressure = str(weather_main["pressure"])
            self.forensics.append(self.current_pressure)
            self.current_humidity = str(weather_main["humidity"])
            self.forensics.append(self.current_humidity)
            #weather_desc = weather_data["weather"] 
            #weather_description = weather_desc[0]["description"] 
        else :
            self.forensics = ["None","None","None"]


    @interactions.extension_command(
        name="weather",
        description="get weather's info of given city",
        options=[
            it.Option(
                name="city_name",
                description="the city's name to look up",
                type=it.OptionType.STRING,
                required=True)
                ]
            )
    async def weather(self,ctx:CC,city_name:str):
        await ctx.defer()
        self.get_weather(city_name)
        await ctx.send("Weather forensics for {} :\nTemperature :{}°C\nPression : {} Pha\nHumidity : {} % ".format(city_name.capitalize(),self.current_temperature,self.current_pressure,self.current_humidity))










def setup(client : Client):
    WeatherWatcher(client)
