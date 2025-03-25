import discord

from config import Config

# Set up the intents for the Discord client (required for certain events)
intents = discord.Intents.default()
intents.message_content = True
intents.guild_scheduled_events = True  # Required for scheduled events

# Initialize the configuration and Discord client
CONFIG = Config()
client = discord.Client(intents=intents)


async def send_event_message(
        entry: discord.AuditLogEntry,
        title: str,
        description: str,
        send_event_link: bool,
        create_discussion_thread: bool
) -> None:
    """
    Helper function to send a message about scheduled events to the configured channel.

    :param entry: The audit log entry for the event. Used to get additional event details.
    :param title: The title of the embed message.
    :param description: The description of the embed message.
    :param send_event_link: Whether to include a link to the event.
    :param create_discussion_thread: Whether to create a discussion thread for the event.
    """
    embed = discord.Embed(title=title, description=description)
    message = await CONFIG.channel.send(embed=embed)  # Send embedded the message for better formatting

    if send_event_link:  # Also send a link to the event to generate a preview
        message = await CONFIG.channel.send(f"[{entry.target.name} Details]({entry.target.url})")

    if create_discussion_thread:
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
        discord.AuditLogAction.scheduled_event_create: {
            "title": "New Event Created",
            "description": "Is it a bird? A plane? No! It's a new team event! See details below!",
            "send_event_link": True,
            "create_discussion_thread": True
        },
        discord.AuditLogAction.scheduled_event_update: {
            "title": "Event Updated",
            "description": f"Hear ye, hear ye! An event was updated! See details below!",
            "send_event_link": True,
            "create_discussion_thread": False
        },
        discord.AuditLogAction.scheduled_event_delete: {
            "title": "Event Cancelled",
            "description": f"Event Name: `{entry.changes.before.name}`\n⎧ᴿᴵᴾ⎫ ❀◟(ᴗ_ ᴗ )",
            "send_event_link": False,
            "create_discussion_thread": False
        },
    }

    if action not in relevant_actions:
        return  # Ignore actions that are not relevant

    await send_event_message(
        entry,
        title=relevant_actions[action]["title"],
        description=relevant_actions[action]["description"],
        send_event_link=relevant_actions[action]["send_event_link"],
        create_discussion_thread=relevant_actions[action]["create_discussion_thread"]
    )


client.run(CONFIG.token)
