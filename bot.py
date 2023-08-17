import os
import discord
import yt_dlp
import asyncio
from discord.ext import commands

TOKEN = 'your_token_here'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user}がログインしました。')

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def play(ctx, url):
    filepath = "/home/ubuntu/temp.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filepath,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    vc = ctx.voice_client
    if vc is None:
        channel = ctx.message.author.voice.channel
        vc = await channel.connect()

    vc.play(discord.FFmpegPCMAudio(filepath), after=lambda e: print('done', e))
    while vc.is_playing():
        await asyncio.sleep(1)

    vc.stop()
    if os.path.exists(filepath):
        os.remove(filepath)

bot.run(TOKEN)
