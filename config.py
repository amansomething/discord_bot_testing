from environs import Env

env = Env()
env.read_env()


class Config:
    """
    Configuration class for the Discord bot.

    Attributes:
        token: The Discord bot token.
        events_channel_id: Channel ID where threads should be created for events ending soon.
        announcements_channel_id: Channel ID where new, updated, and cancelled event announcements should be sent.
        event_check_interval: The interval in minutes to check for scheduled events ending soon.
        event_completion_threshold: How soon (in minutes) upcoming events ending should trigger a thread creation.
        guild: The Discord guild object, initialized after the bot is ready.
        events_channel: The Discord channel object for events, initialized after the bot is ready.
        announcements_channel: The Discord channel object for announcements, initialized after the bot is ready.
    """
    def __init__(self):
        self.token: str = env.str('DISCORD_TOKEN')
        self.events_channel_id: int = env.int('EVENTS_CHANNEL_ID')
        self.announcements_channel_id: int = env.int('ANNOUNCEMENTS_CHANNEL_ID')

        self.event_check_interval: int = 60 # in minutes
        self.event_completion_threshold: int = 30  # in minutes
        self.auto_archive_duration: int = 10080  # 7 days

        self.guild = None
        self.events_channel = None
        self.announcements_channel = None


config = Config()
