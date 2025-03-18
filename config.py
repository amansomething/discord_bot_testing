import discord
from environs import env

env.read_env()


class Config:
    token: str = env.str('DISCORD_TOKEN')
    channel_id: int = env.int('CHANNEL_ID')


config = Config()
intents = discord.Intents.default()

intents.message_content = True
intents.guild_scheduled_events = True  # Required for scheduled events

client = discord.Client(intents=intents)