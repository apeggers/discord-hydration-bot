# bot.py
import os
import asyncio
import logging
import logging.handlers

from dotenv import load_dotenv

import discord
from discord.ext import commands

# Logging Configuration
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s', '%Y-%m-%d %H:%M:%S')

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

# Logfile handler
fh = logging.FileHandler(r'logs/bot.log')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)

log.addHandler(ch)
log.addHandler(fh)

log.info('Initializing...')

# Load Environment Variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('COMMAND_PREFIX')
DELAY = int(os.getenv('REMINDER_DELAY'))

# Hydration Audio File
HYDRATION_AUDIO = r'assets/voice/drink_water.mp3'

log.debug('Notifying on %ss intervals', DELAY)

# List that holds channels to remind
reminders = []


# Discord Bot Code below
bot = commands.Bot(command_prefix=PREFIX)

# Joins voice channel, plays specified audio clip, then leaves
async def say_something(channel: discord.VoiceChannel, fname: str):
    voice_client = await channel.connect()
    voice_client.play(discord.FFmpegPCMAudio(fname, options='-loglevel panic'))
    await asyncio.sleep(2)
    await voice_client.disconnect()

# Task which iterates through list of channels to remind, calls say_something for each
async def reminder_task():
    while True:
        if len(reminders)>0:
            log.info('Reminding %i voice channels to stay hydrated...', len(reminders))
            for channel in reminders:
                await say_something(channel, HYDRATION_AUDIO)

            log.info('Reminders complete. Next round in %i seconds', DELAY)
        else:
            log.info('No active voice channels. Checking again in %i seconds', DELAY)
        
        await asyncio.sleep(DELAY)


# Called when bot is initialized and connects to discord
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='Water Drinking Simulator 1998'))
    log.info('Initialization complete. %s has connected to Discord!', bot.user.name)
    bot.loop.create_task(reminder_task())

# Called anytime someone changes voice state
# This occurs on channel join or leave, mute/deafen status change, etc.
# Adds channels to reminder list when people join, removes them when channels become unpopulated
@bot.event
async def on_voice_state_update(member, before, after):
    if member.name != 'HydrationBot':
        if before.channel != after.channel:
            if before.channel != None and len(before.channel.members) == 0 and before.channel in reminders:
                log.debug('Ending reminders on channel %s', before.channel.name)
                reminders.remove(before.channel)

            if after.channel != None and after.channel not in reminders:
                log.debug('Initializing reminders on channel %s', after.channel.name)
                reminders.append(after.channel)

# Called when user uses prefix with incorrect command
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        log.warn('%s. Caused by user %s in server %s', error, ctx.author.name, ctx.guild.name)
    else:
        raise error


# remindnow command. Runs hydration reminder in user's current voice channel
@bot.command(name='remindnow', help='Reminds everyone in your current voice channel to drink water')
async def remind_now(ctx):
    author = ctx.author
    if author.voice:
        vc = author.voice.channel
        log.info('Manual reminder for user %s in channel %s in server %s', author.name, vc.name, ctx.guild.name)
        await say_something(vc, HYDRATION_AUDIO)
        log.debug('Manual reminder complete')
    else:
        await ctx.send('You must be in a voice channel')


# INITIALIZE
bot.run(TOKEN)