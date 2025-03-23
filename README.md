## Run Locally

Create a `.env` file with the following vars:

```
DISCORD_TOKEN="asdf.ghjkl"
CHANNEL_ID="1234"
```

Run the bot with the following command:

```bash
docker compose up
```

## Deploy to Fly.io
- Run `fly deploy --ha=false` after making the code changes.
- If two machines are deployed can also run `fly scale count 1` to scale down to one machine.

## References
[Discord.py API Reference](https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#)
[Discord Developer Portal](https://discord.com/developers/docs/quick-start/getting-started)