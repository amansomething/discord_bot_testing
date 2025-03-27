from dataclasses import dataclass

import discord

from config import Config

# Set up the intents for the Discord client (required for certain events)
intents = discord.Intents.default()
intents.message_content = True
intents.guild_scheduled_events = True  # Required for scheduled events

# Initialize the configuration and Discord client
CONFIG = Config()
client = discord.Client(intents=intents)


@dataclass
class EventMessage:
    """Dataclass to help organize the parameters for sending messages about scheduled events."""
    title: str  # The title of the message to be sent.
    description: str  # The description of the message to be sent.
    send_event_link: bool = True  # Whether to include a link to the event in the message, which generates a preview.
    create_discussion_thread: bool = False  # Whether to create a discussion thread from the last sent message.

    async def send_event_message(
            self,
            entry: discord.AuditLogEntry,
            channel: discord.TextChannel = None
    ) -> None:
        """
        Send a message about a scheduled event to the given channel.

        :param entry: The audit log entry for the event. Used to get additional event details.
        :param channel: The channel to send the message to. Defaults to the configured channel.
        """
        channel = channel or CONFIG.channel  # Use the provided channel or the default from config

        print(f"Attempting to send message: {self.title} - {self.description}")
        embed = discord.Embed(title=self.title, description=self.description)
        message = await channel.send(embed=embed)  # Send embedded message for better formatting

        if self.send_event_link:  # Also send a link to the event to generate a preview
            print(f"Sending event link: {entry.target.url}")
            message = await channel.send(f"[{entry.target.name} Details]({entry.target.url})")

        if self.create_discussion_thread:
            print(f"Creating discussion thread for message: {message.id}")
            await message.create_thread(
                name=entry.target.name,
                auto_archive_duration=10080  # 7 days
            )


@client.event
async def on_ready() -> None:
    """After the bot is logged in, update the config to set the channel to send messages to."""
    print(f'Logged in as: {client.user}')
    CONFIG.channel = client.get_channel(CONFIG.channel_id)
    print(f'Messages will be sent to: {CONFIG.channel}')
    print('Bot is ready!')


@client.event
async def on_audit_log_entry_create(entry: discord.AuditLogEntry) -> None:
    """
    Check if a relevant event (scheduled event created, updated, or deleted) has occurred.
    Send a message to the team if so.

    https://discordpy.readthedocs.io/en/latest/api.html#discord.on_audit_log_entry_create

    :param entry: The entry that was added to the audit log.
    """
    action = entry.action

    relevant_actions = {
        discord.AuditLogAction.scheduled_event_create: EventMessage(
            title="New Event Created",
            description="Is it a bird? A plane? No! It's a new team event! See details below!",
            create_discussion_thread=True
        ),
        discord.AuditLogAction.scheduled_event_update: EventMessage(
            title="Event Updated",
            description=f"Hear ye, hear ye! An event was updated! See details below!",
        ),
        discord.AuditLogAction.scheduled_event_delete: EventMessage(
            title="Event Cancelled",
            description=f"Event Name: `{entry.changes.before.name}`\n⎧ᴿᴵᴾ⎫ ❀◟(ᴗ_ ᴗ )",
            send_event_link=False,
        ),
    }

    if action not in relevant_actions:
        return  # Ignore actions that are not relevant

    print(f"Relevant action detected: {action}")
    await relevant_actions[action].send_event_message(entry=entry)


client.run(CONFIG.token)
