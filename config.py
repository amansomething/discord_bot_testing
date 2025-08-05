from environs import Env

env = Env()
env.read_env()


class Config:
    """
    Configuration class for the Discord bot.

    Attributes:
        token: The Discord bot token.
        events_channel_id: Channel ID where threads should be created for events ending soon.
        auto_archive_duration: Duration in minutes for auto-archiving discussion threads (default is 7 days).
        guild: The Discord guild object, initialized after the bot is ready.
        events_channel: The Discord channel object for events, initialized after the bot is ready.
    """
    def __init__(self):
        self.token: str = env.str('DISCORD_TOKEN')
        self.events_channel_id: int = env.int('EVENTS_CHANNEL_ID')

        self.auto_archive_duration: int = 10080  # 7 days

        self.guild = None
        self.events_channel = None


config = Config()
