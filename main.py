import discord
from config import config, client


async def send_event_message(message):
    channel = client.get_channel(config.channel_id)
    print(f"Updated channel: {channel}")
    print(f"Sending message: {message}")
    await channel.send(message)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# Check if new event was added
@client.event
async def on_audit_log_entry_create(entry):
    event = entry.target

    if entry.action == discord.AuditLogAction.scheduled_event_create:
        await send_event_message(f"**New event created!**")
        await event_send_details(event)
    elif entry.action == discord.AuditLogAction.scheduled_event_update:
        await send_event_message(f"**An event was updated!**")
        await event_send_details(event)
    elif entry.action == discord.AuditLogAction.scheduled_event_delete:
        await send_event_message(f"Heads up! `{entry.changes.before.name}` has been cancelled!")
    else:
        print("Something else happened that we don't care about.")


async def event_send_details(event):
    """
    https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#discord.ScheduledEvent
    """
    # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    time_format = "%I:%M%p"
    day = event.start_time.strftime("%A, %b %m, %Y")
    start = event.start_time.strftime(time_format)
    end = event.end_time.strftime(time_format)
    message = f"""
**Event**: [{event.name}]({event.url})
**Location**: {event.location}

**Description**: {event.description}

**Time**: {day} @ {start} - {end}
```

"""
    await send_event_message(message)


client.run(config.token)
