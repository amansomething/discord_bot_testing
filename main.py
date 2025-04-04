from datetime import datetime, timezone, timedelta

import discord
from discord.ext import commands, tasks

from config import config
from event_messages import base_messages

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

    print("Setting guild in config...")
    guild = bot.guilds[0]  # Assuming the bot is in only one guild
    if not guild:
        raise ValueError("Bot is not in any guilds.")
    config.guild = guild
    print(f"Updated config with guild: {guild.name}")

    print("Setting channels in config...")
    config.events_channel = bot.get_channel(config.events_channel_id)
    config.announcements_channel = bot.get_channel(config.announcements_channel_id)
    print(f'Threads for events ending soon will be sent to: {config.events_channel}')
    print(f'Event notifications will be sent to: {config.announcements_channel}')

    print("Starting scheduled events check...")
    check_events.start()


@bot.event
async def on_audit_log_entry_create(
        entry: discord.AuditLogEntry,
        channel: discord.TextChannel = None,
        messages: dict = base_messages
):
    """
    Check if a relevant action (scheduled event created, updated, or deleted) has occurred.
    Send a message to the team if so.

    :param entry: The entry that was added to the audit log.
    :param channel: The Discord channel to send messages to. Defaults to the channel from the config.
    :param messages: The dictionary of base messages for different event types. See `event_messages.py`.
    """
    channel = channel or config.announcements_channel  # Use the channel from the config if not provided
    detected_action = entry.action

    relevant_actions = {
        discord.AuditLogAction.scheduled_event_create: "New",
        discord.AuditLogAction.scheduled_event_update: "Updated",
        discord.AuditLogAction.scheduled_event_delete: "Cancelled",
    }

    if detected_action not in relevant_actions:
        return  # Ignore actions that are not relevant

    print(f"Relevant action detected: {detected_action}")

    action = relevant_actions[detected_action]
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
            auto_archive_duration=config.auto_archive_duration,
        )


@tasks.loop(minutes=config.event_check_interval)
async def check_events(guild: discord.Guild = None):
    """
    Checks for scheduled events ending within a threshold and creates a thread if so.

    :param guild: The Discord guild (server) to check for scheduled events.
    """
    guild = guild or config.guild  # Use the guild from config if not provided

    now = datetime.now(timezone.utc)
    print(f"Checking for scheduled events... {now.isoformat()}")
    # Calculate the threshold time for creating a thread
    threshold_time = now + timedelta(minutes=config.event_completion_threshold)

    for event in guild.scheduled_events:
        # Check if the event has an end time and if it falls within the threshold
        ending_soon = event.end_time and now <= event.end_time <= threshold_time

        if not ending_soon:
            print(f"Event '{event.name}' is not ending soon. End time: {event.end_time}")
            continue

        print(f"Event '{event.name}' is ending soon. Creating a discussion thread...")
        channel = config.events_channel
        month_year = event.end_time.strftime("%m/%d")  # Ex. "12/31" for December 31st
        thread_name = f"{event.name} - ({month_year})"  # Ex. "Snek Den - (12/31)"
        thread = await channel.create_thread(
            name=thread_name,
            type=discord.ChannelType.public_thread,
            auto_archive_duration=config.auto_archive_duration
        )
        await thread.send(f"`{event.name}` is ending soon! Discuss here!")
        print(f"Created discussion thread '{thread_name}' for event '{event.name}' with ID {event.id}.")

    print(f"Finished checking for scheduled events. Will check again in: {config.event_check_interval} minutes\n")


check_events.before_loop(bot.wait_until_ready)
bot.run(config.token)
