# bot.py
import os
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('COMMAND_PREFIX')
DELAY = int(os.getenv('REMINDER_DELAY'))

bot = commands.Bot(command_prefix=PREFIX)

reminders = []

async def reminder_task():
    while True:
        #reminders_string = ''
        for channel in reminders:
            voice_client = await channel.connect()
            voice_client.play(discord.FFmpegPCMAudio('drink_water.mp3'), after=lambda e: print('done', e))
            await asyncio.sleep(2)
            await voice_client.disconnect()
            #reminders_string = reminders_string + '\t- ' + channel.name + '\n'
        #print(f'Reminding:\n{reminders_string}')
        await asyncio.sleep(DELAY)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    bot.loop.create_task(reminder_task())

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        if before.channel != None and len(before.channel.members) == 0 and before.channel in reminders:
            print(f'Ending reminders on channel {before.channel.name}')
            reminders.remove(before.channel)

        if after.channel != None and after.channel not in reminders:
            print(f'Initializing reminders on channel {after.channel.name}')
            reminders.append(after.channel)

@bot.command(name='test', help='Generates a simple test response')
async def test_cmd(ctx):
    await ctx.send('Ross sucks')


bot.run(TOKEN)