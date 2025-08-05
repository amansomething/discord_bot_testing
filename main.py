import discord
from discord.ext import commands

from config import config

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
    print(f'Notifications will be sent to: {config.events_channel}')


@bot.event
async def on_audit_log_entry_create(
        entry: discord.AuditLogEntry,
        channel: discord.TextChannel = None,
):
    """
    Check if a relevant action (scheduled event created or deleted) has occurred.
    Send a message to the team if so.

    :param entry: The entry that was added to the audit log.
    :param channel: The Discord channel to send messages to. Defaults to the channel from the config.
    """
    channel = channel or config.events_channel  # Use the channel from the config if not provided
    detected_action = entry.action

    relevant_actions = {
        discord.AuditLogAction.scheduled_event_create: "New",
        discord.AuditLogAction.scheduled_event_delete: "Cancelled",
    }

    if detected_action not in relevant_actions:
        return  # Ignore actions that are not relevant

    print(f"Relevant action detected: {detected_action}")

    action = relevant_actions[detected_action]
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
        title = f"Event Cancelled"
        description = f"Event Name: `{name}`\n⎧ᴿᴵᴾ⎫ ❀◟(ᴗ_ ᴗ )"
        embed = discord.Embed(title=title, description=description)
        await channel.send(embed=embed)  # Send embedded message for better formatting
    else:
        print(f"Sending event link: {url}")
        sent_message = await channel.send(f"[{name} Details]({url})")
        print(f"Creating discussion thread for message: {sent_message.id}")
        await sent_message.create_thread(
            name=name,
            auto_archive_duration=config.auto_archive_duration,
        )

bot.run(config.token)
