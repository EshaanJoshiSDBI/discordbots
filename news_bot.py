import discord
import os
from GoogleNews import GoogleNews
from discord.embeds import Embed
import pandas as pd
from tabulate import tabulate
from datetime import datetime as dt
news = GoogleNews(start = dt.today(), end = dt.today())
bot = discord.Client()
embed = discord.Embed()
@bot.event
async def on_ready():
    print("I'm on as {}".format(bot))
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!{}'.format(message.author))
    if message.content.startswith('news:'):
        string = str(message.content)
        # print(string)
        topic = ''.join([i for i in string.split(':')[1] if not i.isdigit()]).rstrip()
        # num = [int(i) for i in string.split() if i.isdigit()][0]
        news.get_news(topic)
        x = pd.DataFrame(news.results())
        news.clear()
        x = x[['title','desc','link','img']].sample()
        msg = discord.Embed(title = list(x.title)[0],url = 'http://' + list(x.link)[0],description = list(x.desc)[0])
        link = list(x.img)[0]
        msg.set_thumbnail(url = link)
        if len(x) == 0:
            await message.channel.send('No latest news')
        else:
            await message.channel.send(embed = msg)
bot.run(os.getenv('TOKEN'))