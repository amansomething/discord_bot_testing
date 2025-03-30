from pathlib import Path

from environs import Env

env = Env()
env.read_env()


class Config:
    """
    Configuration class for the Discord bot.

    Attributes:
        token: The Discord bot token.
        channel_id: The ID of the channel to send messages to.
        event_check_interval: The interval in hours to check for scheduled events.
        event_completion_threshold: The threshold in hours for upcoming events to create a discussion thread about.
        events_data_file: The path to the JSON file used to store event data for later reference.
        guild: The Discord guild object, initialized after the bot is ready.
        channel: The Discord channel object, initialized after the bot is ready.
    """
    def __init__(self):
        self.token: str = env.str('DISCORD_TOKEN')
        self.channel_id: int = env.int('CHANNEL_ID')
        self.event_check_interval: int = 24 # in hours
        self.event_completion_threshold: int = 3  # in hours
        self.events_data_file: Path = Path("events_data.json")
        self.guild = None
        self.channel = None

    def initialize_data_file(self):
        """
        Initialize the events data file if it does not exist.
        The file is used to store event info for later reference without making API calls.
        """
        if not self.events_data_file.exists():
            print("Initializing events data file...")
            with open(self.events_data_file, 'w') as f:
                f.write("{}")

config = Config()
