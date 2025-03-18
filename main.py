import discord
from config import config, client


async def send_event_message(channel, name, message):
    print(f"Sending message: {message}")
    await channel.send(f"{message}: **{name}**")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# Check if new event was added
@client.event
async def on_audit_log_entry_create(entry):
    event = entry.target
    channel = client.get_channel(config.channel_id)

    if entry.action == discord.AuditLogAction.scheduled_event_create:
        await send_event_message(channel, event.name, "A new event was created")
    elif entry.action == discord.AuditLogAction.scheduled_event_update:
        await send_event_message(channel, event.name, "The event was updated")
    elif entry.action == discord.AuditLogAction.scheduled_event_delete:
        name = entry.changes.before.name
        print(f"{entry.changes} event was deleted")
        await send_event_message(channel, name, "The event was deleted")
    else:
        print("Something else happened that we don't care about.")


client.run(config.token)
