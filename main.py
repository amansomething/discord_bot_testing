import discord
from config import config, client


@client.event
async def on_ready() -> None:
    """Log in as the user and set the channel to send messages to."""
    print(f'Logged in as: {client.user}')
    config.set_channel()
    print(f'Messages will be sent to: {config.channel}')


@client.event
async def on_audit_log_entry_create(entry):
    """
    Check if a new event was added, updated, or deleted.
    Send a message to the channel if any of these actions occur.

    :param entry: discord.AuditLogEntry - The entry that was created
    """
    channel = config.channel
    event = entry.target

    if entry.action == discord.AuditLogAction.scheduled_event_create:
        message = f"**New event created!**\n{event.url}"
    elif entry.action == discord.AuditLogAction.scheduled_event_update:
        message = f"**An event was updated!**\n{event.url}"
    elif entry.action == discord.AuditLogAction.scheduled_event_delete:
        message = f"Heads up! `{entry.changes.before.name}` has been cancelled!"
    else:
        print("Something else happened that we don't care about.")
        return None

    await channel.send(message)


client.run(config.token)
