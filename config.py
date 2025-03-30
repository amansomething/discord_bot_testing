from environs import Env

env = Env()
env.read_env()


# TODO: Update to handle multiple channels (one for announcements, one for completed event threads)
class Config:
    """
    Configuration class for the Discord bot.

    Attributes:
        token: The Discord bot token.
        channel_id: The ID of the channel to send messages to.
        event_check_interval: The interval in hours to check for scheduled events.
        event_completion_threshold: The threshold in minutes for upcoming events to create a discussion thread about.
        guild: The Discord guild object, initialized after the bot is ready.
        channel: The Discord channel object, initialized after the bot is ready.
    """
    def __init__(self):
        self.token: str = env.str('DISCORD_TOKEN')
        self.channel_id: int = env.int('CHANNEL_ID')
        self.event_check_interval: int = 24 # in hours
        self.event_completion_threshold: int = 30  # in minutes  TODO: update after testing is complete
        self.auto_archive_duration: int = 10080  # 7 days
        self.guild = None
        self.channel = None


config = Config()
