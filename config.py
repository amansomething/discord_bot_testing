import discord
from environs import env

env.read_env()


class Config:
    token: str = env.str('DISCORD_TOKEN')
    channel_id: int = env.int('CHANNEL_ID')
    channel = None  # Where to send messages. Needs to be initialized after bot is logged in.

    def set_channel(self, channel_id=None):
        """
        Sets the channel where messages will be sent.
        Uses the channel_id set in the Config unless specified otherwise.

        :param channel_id: int - The channel ID to send messages to
        """
        if channel_id is None:
            channel_id = self.channel_id
        self.channel = client.get_channel(channel_id)


config = Config()
intents = discord.Intents.default()

intents.message_content = True
intents.guild_scheduled_events = True  # Required for scheduled events

client = discord.Client(intents=intents)
