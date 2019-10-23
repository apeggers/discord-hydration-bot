# utils.py
import discord

class ServerSet:

    def __init__(self, channel:discord.VoiceChannel = None):
        self.guild = channel.guild
        self.channels = [] if channel is None else [channel]

    def __iter__(self):
        return iter(self.channels)

    def __eq__(self, other: discord.Guild):
        return other == self.guild

    def __contains__(self, channel:discord.VoiceChannel):
        return channel in self.channels

    def __len__(self):
        return len(self.channels)
    
    def add_channel(self, channel: discord.VoiceChannel):
        if channel not in self.channels:
            self.channels.append(channel)

    def remove_channel(self, channel: discord.VoiceChannel):
        self.channels.remove(channel)

class ReminderSet:

    def __init__(self, channel:discord.VoiceChannel = None):
        self.guilds = [] if channel is None else [ServerSet(channel)]
    
    def __iter__(self):
        return iter(self.guilds)

    def __contains__(self, other:discord.VoiceChannel):
        for serverSet in self.guilds:
            if other in serverSet:
                return True
        return False

    def __len__(self):
        l = 0
        for serverSet in self.guilds:
            l = l + len(serverSet)
        return l
    
    def add_channel(self, channel:discord.VoiceChannel):
        for serverSet in self.guilds:
            if serverSet == channel.guild:
                serverSet.add_channel(channel)
                return
        self.guilds.append(ServerSet(channel))
    
    def remove_channel(self, channel:discord.VoiceChannel):
        for serverSet in self.guilds:
            if serverSet == channel.guild:
                serverSet.remove_channel(channel)
                return

