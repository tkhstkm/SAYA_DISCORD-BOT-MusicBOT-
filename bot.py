import os
import discord
import yt_dlp
import asyncio
from discord.ext import commands

TOKEN = ''

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
    filepath_without_extension = "/home/ubuntu/temp"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filepath_without_extension,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # 既存のファイルがあれば削除
    if os.path.exists(filepath_without_extension + ".mp3"):
        os.remove(filepath_without_extension + ".mp3")

    # ダウンロード
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # 再生の準備
    vc = ctx.voice_client
    if vc is None:
        channel = ctx.message.author.voice.channel
        vc = await channel.connect()

    # 再生
    vc.play(discord.FFmpegPCMAudio(filepath_without_extension + ".mp3"), after=lambda e: print('done', e))
    while vc.is_playing():
        await asyncio.sleep(1)

    # 停止
    vc.stop()

    # ファイル削除
    if os.path.exists(filepath_without_extension + ".mp3"):
        os.remove(filepath_without_extension + ".mp3")


bot.run(TOKEN)
