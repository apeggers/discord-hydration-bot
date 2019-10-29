# discord-hydration-bot (WIP)

## Description
This is the code behind HydrationBot, a Discord bot that reminds gamers to stay hydrated. If HydrationBot is active on your Discord server, it will join active voice channels on a fixed interval and play an audio clip with a friendly reminder to stay hydrated. Currently, functionality is very basic. See to-do list below for future plans.

## Adding HydrationBot to your server
HydrationBot is currently a work in progress and is not designed for deployment on multiple Discord servers. Check back for progress

In the meantime, you can clone this repository and run the bot on your own computer as detailed below.

## Usage and Dependencies

Before running the bot, the following are required:
- Python 3.6
- Pipenv
- FFmpeg (binaries must be on PATH)
- An activated Discord bot with known token (see Discord developer tools)

Additionally, create a `.env` file in the base directory with the following information (without square brackets):
```
DISCORD_TOKEN=[your Discord bot token]
COMMAND_PREFIX=[prefix string for text commands]
REMINDER_DELAY=[seconds between reminders]
```
To configure the Python virtual environment, run `$ pipenv install` from the project base directory:

To run the bot, simply execute the following command from the base directory:
```
$ pipenv run python bot.py
```

## To-do

- [x] Add improved logging framework (log to file and console)
- [x] Store channel list in data structure iterable by server
- [x] Iterate servers asynchronously when running reminders, iterate channels in each server synchronously
- [ ] Add command for listing channels with active reminders and time to next reminder
- [ ] Change notifications to channel-specific timers
- [x] Add command to remind user's current channel now
- [ ] Add command to prevent reminders on specific channel for set time
- [ ] Add framework for server-specific settings and commands to change them
- [ ] Add blacklisting for specific channels
- [ ] Add blacklisting for specific users (e.g. don't notify bots in channels alone)
- [ ] Move data and settings to relational database
- [ ] Additional checks? (e.g. posture check, vibe check, etc.)
- [ ] Make bot public???
- [ ] Profit????????