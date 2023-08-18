import os
import discord
import yt_dlp
import asyncio
from discord.ext import commands

TOKEN = 'discord_token'
AUTHORIZED_USER_ID = owner_user_id

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

music_queue = []

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
    global music_queue
    music_queue.append(url)
    if not ctx.voice_client.is_playing():
        await play_next(ctx)

@bot.command()
async def queue(ctx):
    queue_str = "\n".join([f"{idx+1}. {url}" for idx, url in enumerate(music_queue)])
    await ctx.send(f"待機中の楽曲:\n{queue_str}")

@bot.command()
async def shutdown(ctx):
    if ctx.author.id == AUTHORIZED_USER_ID:
        await bot.close()
    else:
        await ctx.send("シャットダウン権限がありません。")

async def play_next(ctx):
    global music_queue
    if music_queue:
        url = music_queue.pop(0)
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

        if os.path.exists(filepath_without_extension + ".mp3"):
            os.remove(filepath_without_extension + ".mp3")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        vc = ctx.voice_client
        if vc is None:
            channel = ctx.message.author.voice.channel
            vc = await channel.connect()

        vc.play(discord.FFmpegPCMAudio(filepath_without_extension + ".mp3"), after=lambda e: play_next_coro(ctx))
        while vc.is_playing():
            await asyncio.sleep(1)

        if os.path.exists(filepath_without_extension + ".mp3"):
            os.remove(filepath_without_extension + ".mp3")

def play_next_coro(ctx):
    bot.loop.create_task(play_next(ctx))

bot.run(TOKEN)
