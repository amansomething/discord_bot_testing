import discord

from config import Config

# Set up the intents for the Discord client (required for certain events)
intents = discord.Intents.default()
intents.message_content = True
intents.guild_scheduled_events = True  # Required for scheduled events

# Initialize the configuration and Discord client
CONFIG = Config()
client = discord.Client(intents=intents)


@client.event
async def on_ready() -> None:
    """After the bot is logged in, update the config to set the channel to send messages to."""
    print(f'Logged in as: {client.user}')
    CONFIG.channel = client.get_channel(CONFIG.channel_id)
    print(f'Messages will be sent to: {CONFIG.channel}')


@client.event
async def on_audit_log_entry_create(entry) -> None:
    """
    Check if a new event was added, updated, or deleted.
    Send a message to the channel if any of these actions occur.

    :param entry: The entry that was added to the audit log.
    """
    action = entry.action

    relevant_actions = {
        "new": discord.AuditLogAction.scheduled_event_create,
        "updated": discord.AuditLogAction.scheduled_event_update,
        "cancelled": discord.AuditLogAction.scheduled_event_delete,
    }

    if action not in relevant_actions.values():
        # We don't care about this action, so ignore it.
        return None

    if action == relevant_actions["cancelled"]:
        message = f"**Heads up!** An event has been cancelled.\nEvent: `{entry.changes.before.name}`\n⎧ᴿᴵᴾ⎫ ❀◟(ᴗ_ ᴗ )\n"
    elif action == relevant_actions["new"]:
        message = f"**Is that a bird? A plane? No!** It's a new team [event]({entry.target.url})!\n"
    else:
        message = f"**Hear ye, hear ye! An [event]({entry.target.url}) was updated!**\n"

    await CONFIG.channel.send(message)


client.run(CONFIG.token)
