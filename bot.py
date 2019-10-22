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

log.debug('Notifying on %ss intervals', DELAY)

# List that holds channels to remind
reminders = []


# Discord Bot Code below
bot = commands.Bot(command_prefix=PREFIX)

async def reminder_task():
    while True:
        if len(reminders)>0:
            log.info('Reminding %i voice channels to stay hydrated...', len(reminders))
            for channel in reminders:
                voice_client = await channel.connect()
                voice_client.play(discord.FFmpegPCMAudio('assets/voice/drink_water.mp3', options='-loglevel panic'))
                await asyncio.sleep(2)
                await voice_client.disconnect()

            log.info('Reminders complete. Next round in %i seconds', DELAY)
        else:
            log.info('No active voice channels. Checking again in %i seconds', DELAY)
        
        await asyncio.sleep(DELAY)


@bot.event
async def on_ready():
    log.info('Initialization complete. %s has connected to Discord!', bot.user.name)
    bot.loop.create_task(reminder_task())


@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        if before.channel != None and len(before.channel.members) == 0 and before.channel in reminders:
            log.debug('Ending reminders on channel %s', before.channel.name)
            reminders.remove(before.channel)

        if after.channel != None and after.channel not in reminders:
            log.debug('Initializing reminders on channel %s', after.channel.name)
            reminders.append(after.channel)


@bot.command(name='test', help='Generates a simple test response')
async def test_cmd(ctx):
    await ctx.send('Ross sucks')


bot.run(TOKEN)