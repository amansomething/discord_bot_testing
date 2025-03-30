from datetime import datetime, timezone, timedelta

import discord
from discord.ext import commands, tasks

from config import config
# from event_checker import check_events
from event_messages import base_messages

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

    print("Checking guild...")
    guild = bot.guilds[0]  # Assuming the bot is in only one guild
    if not guild:
        raise ValueError("Bot is not in any guilds.")
    config.guild = guild
    print(f"Updated config with guild: {guild.name}")

    print("Checking messages channel...")
    config.channel = bot.get_channel(config.channel_id)
    print(f'Messages will be sent to: {config.channel}')

    print("Starting scheduled events check...")
    check_events.start()  # Start the scheduled event checker


@bot.event
async def on_audit_log_entry_create(
        entry: discord.AuditLogEntry,
        channel: discord.TextChannel = None,
        messages: dict = base_messages
):
    """
    Check if a relevant event (scheduled event created, updated, or deleted) has occurred.
    Logs the event and can later be expanded to notify a team channel.

    :param entry: The entry that was added to the audit log.
    :param channel: The Discord channel to send messages to. Defaults to the channel from the config.
    :param messages: The dictionary of base messages for different event types. See `event_messages.py`.
    """
    channel = channel or config.channel  # Use the channel from the config if not provided
    detected_action = entry.action

    relevant_actions = {
        discord.AuditLogAction.scheduled_event_create: "New",
        discord.AuditLogAction.scheduled_event_update: "Updated",
        discord.AuditLogAction.scheduled_event_delete: "Cancelled",
    }

    if detected_action not in relevant_actions:
        return  # Ignore actions that are not relevant

    action = relevant_actions[detected_action]
    print(f"Relevant action detected: {action}")
    message = messages[action]

    url = entry.target.url if hasattr(entry.target, 'url') else None

    if hasattr(entry.target, 'name'):
        name = entry.target.name
    else:
        try:
            name = entry.changes.before.name
        except AttributeError:
            name = "Unknown Event Name"  # Fallback if no name is available
            print("Failed to retrieve event name from entry, using fallback.")

    if action == "Cancelled":
        message.description = f"Event Name: `{name}`\n⎧ᴿᴵᴾ⎫ ❀◟(ᴗ_ ᴗ )"

    embed = discord.Embed(title=message.title, description=message.description)
    sent_message = await channel.send(embed=embed)  # Send embedded message for better formatting

    if message.send_event_link:  # Also send a link to the event to generate a preview
        print(f"Sending event link: {url}")
        sent_message = await channel.send(f"[{name} Details]({url})")

    if message.create_discussion_thread:
        print(f"Creating discussion thread for message: {sent_message.id}")
        await sent_message.create_thread(
            name=name,
            auto_archive_duration=10080  # 7 days
        )


@tasks.loop(minutes=5)  # TODO: Update after testing is complete
async def check_events(
        guild: discord.Guild = None
):
    """
    Checks for scheduled events ending within the threshold and creates a thread if needed.

    :param guild: The Discord guild (server) to check for scheduled events.
    """
    guild = guild or config.guild  # Use the guild from config if not provided

    now = datetime.now(timezone.utc)
    print(f"Checking for scheduled events... {now.isoformat()}")
    # Calculate the threshold time for checking events
    threshold_time = now + timedelta(hours=config.event_completion_threshold)

    for event in guild.scheduled_events:
        print(event)
        # Check if the event has an end time and if it falls within the threshold
        if event.end_time and now <= event.end_time <= threshold_time:
            print(f"Event '{event.name}' is ending soon.")
        else:
            print(f"Event '{event.name}' is not ending soon. Current time: {now.isoformat()}")

check_events.before_loop(bot.wait_until_ready)
bot.run(config.token)
