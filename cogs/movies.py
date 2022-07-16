import interactions 
import interactions as it
from interactions import Client, Button, ButtonStyle, SelectMenu, SelectOption, ActionRow
from interactions import CommandContext as CC
from interactions import ComponentContext as CPC
import requests
from bs4 import BeautifulSoup

class Watcher(interactions.Extension):
    def __init__(self,client : Client) -> None:
        self.movies_info = {}
        return





    def search(self,ctx:CC,_movie_name:str):
        """search for a movie name in Mycima.Cloud"""
        _movie_name = _movie_name.replace(" ","+")
        result = requests.get("https://mycima.cloud/search/" + _movie_name)
        src = result.content
        soup = BeautifulSoup(src, "html.parser")
        self.movies_info[str(ctx.author.id)] = soup.find_all("div",{"class":"Thumb--GridItem"})

    def get_links(self,_main_link:str) -> list[str]:
        """get different qualities download links from a download page"""
        _mini_links = []
        _result = requests.get(_main_link)
        _src = _result.content
        _soup = BeautifulSoup(_src, "html.parser")
        _movies = _soup.find_all("a",{"class":"hoverable activable"})
        for _movie in _movies :
            if "upbam" in _movie['href']:
                _mini_links.append(_movie['href'])
        return _mini_links

    def get_qualities(self,_movies_links_list:list[str]) -> dict:
        """convert list of movies links to a dict as {quality:link}"""
        qualities = ["280p", "360p", "480p", "720p", "1080p", "1440p", "2160p", "2k", "4k", "8k" ]
        _movies_dict = {}
        for _movie in _movies_links_list:
            for quality in qualities:
                if quality in _movie:
                    _movies_dict[quality] = _movie
        return _movies_dict

    def create_movies_list(self,user_id:str) -> SelectMenu:
        """create SelectMenu for the movie's search result"""
        movies_list = self.movies_info[user_id]
        temp_list = []
        for order in range(len(movies_list)):
            temp_list.append(it.SelectOption(
                                            label=movies_list[order].text,
                                            value=str(order)
                                            )
                            )
        temp_list.append(it.SelectOption(
                                        label="Cancel",
                                        value="Cancel"
                                        )
                        )
        menu = it.SelectMenu(
                        options=temp_list,
                        placeholder="Select Movie !",
                        custom_id=f"select_movie-{user_id}"
                            )
        return menu

    def create_dl_buttons(self,links:dict) -> list[Button]:
        """convert a dict of {quality:link} to a list of links buttons"""
        _buttons = []
        if len(links) <= 5:
            for link in links:
                _button = Button(
                                style=ButtonStyle.LINK, 
                                label=link, 
                                url=links[link],
                                disabled=False
                                )
                _buttons.append(_button)
        elif len(links) > 5:
            for link in links:
                _button = Button(
                                style=ButtonStyle.LINK, 
                                label=link, 
                                url=links[link],
                                disabled=False
                                )
                _buttons.append(_button)
                if len(_buttons) == 5 :
                    break

        return _buttons


    @interactions.extension_command(
                                    name="watch_movie",
                                    description="search for a movie on MyCima website and get download links",
                                    options=[
                                            it.Option(
                                                    name="movie_name",
                                                    description="the movie name",
                                                    type=it.OptionType.STRING,
                                                    required=True
                                                    )
                                            ]   
                                    )
    async def watch_movie(self,ctx:CC,movie_name:str):
        await ctx.defer()
        self.search(ctx,movie_name)
        if len(self.movies_info[str(ctx.author.user.id)]) > 0 :
            movies_menu = self.create_movies_list(str(ctx.author.id))
            await ctx.send("Choose your movie",components=[movies_menu])
        else:
            await ctx.send("Didn't found what you asked for :c, try another term.")

    @interactions.extension_listener()
    async def on_component(self,ctx:CPC):
        if ctx.custom_id.startswith("select_movie-"):
            _user_id = ctx.custom_id.split("-")[1]
            if _user_id == str(ctx.user.id):
                _choice_ord = int(ctx.data.values[0])
                _chosen_movie = self.movies_info[_user_id][_choice_ord]
                _dl_link = _chosen_movie.find("a").attrs['href']
                _links_list = self.get_links(_dl_link)
                _final_links = self.get_qualities(_links_list)
                _buttons = self.create_dl_buttons(_final_links)
                await ctx.edit("Choose your prefered quality !",components=_buttons)
                self.movies_info.pop(_user_id)
            else:
                await ctx.send("Don't touch what's not yours >:c .",ephemeral=True)










def setup(client : Client):
    Watcher(client)
