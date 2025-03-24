import discord

from config import config, client


@client.event
async def on_ready() -> None:
    """Log in as the user and set the channel to send messages to."""
    print(f'Logged in as: {client.user}')
    config.set_channel()
    print(f'Messages will be sent to: {config.channel}')


@client.event
async def on_audit_log_entry_create(entry) -> None:
    """
    Check if a new event was added, updated, or deleted.
    Send a message to the channel if any of these actions occur.

    :param entry: The entry that was added to the audit log.
    """
    channel = config.channel
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
        message = f"**Heads up!** `{entry.changes.before.name}` **has been cancelled! ⎧ᴿᴵᴾ⎫ ❀◟(ᴗ_ ᴗ )**"
    elif action == relevant_actions["new"]:
        message = f"**Is that a bird? A plane? No!** It's a new team [event]({entry.target.url})!"
    else:
        message = f"**Hear ye, hear ye! An [event]({entry.target.url}) was updated!**"

    await channel.send(message)


client.run(config.token)
