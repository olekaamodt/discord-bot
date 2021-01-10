import os
import requests
import xml.etree.ElementTree as ET
import discord
from discord.ext import commands
from looter import get_random_picture
import youtube_dl
import asyncio
import json
from just_eat_scraper import FoodDelivery

jsonData = open("token.json")
tokenObj = json.load(jsonData)
jsonData.close()

path = os.path.dirname(os.path.abspath(__file__))

bot_token = tokenObj['DISCORD_TOKEN']
guild_name = tokenObj["DISCORD_GUILD"]
bot = discord.Client()




def get_rss_feed(url):
    response = requests.get(url)

    with open("news.xml", "wb") as file:
        file.write(response.content)

    tree = ET.parse("news.xml")
    root = tree.getroot()
    link_list = []
    for element in root.findall("./channel/item/link"):
        link_list.append(element.text)

    return link_list




class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)



class food_order(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()



food = FoodDelivery()


#async def on_member_join(member):
    #print(member.guild.voice_channels)
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    
@bot.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        

    if message.content.startswith('!food'):
        message.channel.send("kukkern12")
        print(message.content[6:10])
        

      
bot.run(bot_token)
