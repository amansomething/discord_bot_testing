from discord import TextChannel
from environs import env

env.read_env()


class Config:
    """
    Configuration class for the Discord bot.

    Attributes:
        token: The Discord bot token.
        channel_id: The ID of the channel to send messages to.
        channel: The Discord channel object, initialized after the bot is ready.
    """
    def __init__(self):
        self.token: str = env.str('DISCORD_TOKEN')  # Discord bot token
        self.channel_id: int = env.int('CHANNEL_ID')  # Channel ID to send messages to
        self.channel: TextChannel | None = None

