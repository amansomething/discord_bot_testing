from pathlib import Path

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
        events_file: The path to the JSON file for storing events.
    """
    def __init__(self):
        self.token: str = env.str('DISCORD_TOKEN')
        self.channel_id: int = env.int('CHANNEL_ID')
        self.channel: TextChannel | None = None
        self.events_file: str = 'events.json'
        self.initialize_events_file()

    def initialize_events_file(self):
        """Initialize the events file if it does not exist."""
        if not Path(self.events_file).exists():
            print("Initializing events file...")
            with open(self.events_file, 'w') as f:
                f.write('[]')
