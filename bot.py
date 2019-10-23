# bot.py

import os
import asyncio
import logging
import logging.handlers

from dotenv import load_dotenv

import discord
from discord.ext import commands

from utils import ReminderSet

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

# Audio Files
HYDRATION_AUDIO = r'assets/voice/drink_water.mp3'
VIBE_CHECK_AUDIO = r'assets/voice/vibe_check.mp3'
POSTURE_CHECK_AUDIO = r'assets/voice/posture_check.mp3'

log.debug('Notifying on %ss intervals', DELAY)

# List that holds channels to remind
reminders = ReminderSet()


# Discord Bot Code below
bot = commands.Bot(command_prefix=PREFIX)


async def say_something(channel: discord.VoiceChannel, fname: str, dur: float):
    '''Joins voice channel, plays audio clip, then leaves
    
    Arguments:
        channel {discord.VoiceChannel} -- the channel to join
        fname {str} -- path to audio file
        dur {float} -- duration in seconds
    '''
    voice_client = await channel.connect()
    voice_client.play(discord.FFmpegPCMAudio(fname, options='-loglevel panic'))
    await asyncio.sleep(dur)
    await voice_client.disconnect()


async def reminder_task():
    '''Runs hydration reminder for each channel in reminders list.

    Must be added to bot loop with bot.loop.create_task(reminder_task())
    '''
    while True:
        if len(reminders)>0:
            log.info('Reminding %i voice channels to stay hydrated...', len(reminders))
            for server in reminders:
                await asyncio.sleep(0)
                for channel in server:
                    await say_something(channel, HYDRATION_AUDIO, 2)

            log.info('Reminders complete. Next round in %i seconds', DELAY)
        else:
            log.info('No active voice channels. Checking again in %i seconds', DELAY)
        
        await asyncio.sleep(DELAY)


@bot.event
async def on_ready():
    '''Initialization tasks. Function called when Discord connection established.
    '''
    await bot.change_presence(activity=discord.Game(name='Water Drinking Simulator 1998'))
    log.info('Initialization complete. %s has connected to Discord!', bot.user.name)
    bot.loop.create_task(reminder_task())


@bot.event
async def on_voice_state_update(member, before, after):
    '''Gets called when someone changes voice state.

    Adds channels to reminder list when people join, removes them when channel is empty.

    Occurs on join/leave, mute/deafen change, etc.
    
    Arguments:
        member {discord.Member} -- The member object (specific user in guild)
        before {discord.VoiceState} -- VoiceState before change
        after {discord.VoiceState} -- VoiceState after change
    '''
    if member.name != 'HydrationBot':
        if before.channel != after.channel:
            if before.channel != None and len(before.channel.members) == 0 and before.channel in reminders:
                log.debug('Ending reminders on channel %s', before.channel.name)
                reminders.remove_channel(before.channel)

            if after.channel != None and after.channel not in reminders:
                log.debug('Initializing reminders on channel %s', after.channel.name)
                reminders.add_channel(after.channel)


@bot.event
async def on_command_error(ctx, error):
    '''Called when a user uses command prefix with an incorrect command
    
    Arguments:
        ctx {discord.ext.commands.Context} -- context of message that caused error
        error {discord.ext.commands.CommandError} -- the error
    
    Raises:
        {discord.ext.commands.CommandError}: if error isn't CommandNotFound error
    '''
    if isinstance(error, commands.CommandNotFound):
        log.warn('%s. Caused by user %s in server %s', error, ctx.author.name, ctx.guild.name)
    else:
        raise error


@bot.command(name='remindnow', help='Reminds everyone in your current voice channel to drink water')
async def remind_now(ctx):
    '''Runs hydration reminder in invoking user's current voice channel

    Does not add channel to reminder list.
    
    Arguments:
        ctx {discord.ext.commands.Context} -- context of invoking message
    '''
    author = ctx.author
    if author.voice is None:
        await ctx.send('You must be in a voice channel')
    else:
        vc = author.voice.channel
        log.info('Manual reminder for user %s in channel %s in server %s', author.name, vc.name, ctx.guild.name)
        await say_something(vc, HYDRATION_AUDIO, 2)
        log.debug('Manual reminder complete')

@bot.command(name='vibecheck', help='Calls for vibe check in your current voice channel')
async def vibe_check(ctx):
    '''Runs vibe check in invoking user's current voice channel
    
    Arguments:
        ctx {discord.ext.commands.Context} -- context of invoking message
    '''
    author = ctx.author
    if author.voice is None:
        await ctx.send('You must be in a voice channel')
    else:
        vc = author.voice.channel
        log.info('Vibe check for user %s in channel %s in server %s', author.name, vc.name, ctx.guild.name)
        await say_something(vc, VIBE_CHECK_AUDIO, 4.20)
        log.debug('Vibe check complete')

@bot.command(name='posturecheck', help='Calls for posture check in your current voice channel')
async def posture_check(ctx):
    '''Runs posture check in invoking user's current voice channel
    
    Arguments:
        ctx {discord.ext.commands.Context} -- context of invoking message
    '''
    author = ctx.author
    if author.voice is None:
        await ctx.send('You must be in a voice channel')
    else:
        vc = author.voice.channel
        log.info('Posture check for user %s in channel %s in server %s', author.name, vc.name, ctx.guild.name)
        await say_something(vc, POSTURE_CHECK_AUDIO, 4.5)
        log.debug('Posture check complete')

# INITIALIZE
bot.run(TOKEN)