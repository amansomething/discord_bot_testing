# Discord Bot Testing with Fly.io

A simple Discord bot that notifies a channel when an event is added, updated, or deleted from a server.

<!-- TOC -->
* [Local Testing](#local-testing)
  * [Pre-requisites](#pre-requisites)
  * [Run Locally](#run-locally)
* [Update Cloud Deployment](#update-cloud-deployment)
  * [Directly on Fly.io](#directly-on-flyio)
  * [Using GitHub Actions](#using-github-actions)
* [References](#references)
<!-- TOC -->

## Local Testing

### Pre-requisites

- Discord Bot Token (See: https://discord.com/developers/docs/quick-start/getting-started)
- Discord Channel ID (Last part of the channel URL, e.g., `https://discord.com/channels/123/5678` -> `5678`)

### Run Locally

Create a `.env` file with the following vars:

```
DISCORD_TOKEN="asdf.ghjkl"
CHANNEL_ID="1234"
```

Run the bot with the following command:

```bash
docker compose up
```

## Update Cloud Deployment

### Directly on Fly.io

- Run `fly deploy` after making the code changes.
- If two machines end up being deployed, scale down using `fly scale count 1`.

**Note**: Fly.io only uses the `Dockerfile` and ignores the `compose.yml` file.
### Using GitHub Actions

- Github Actions are set up to automatically deploy the bot to Fly.io on every push to the `main` branch.

## References

- [Discord.py API Reference](https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#)
- [Discord Developer Portal](https://discord.com/developers/docs/quick-start/getting-started)
- [Fly.io Github Actions Documentation](https://fly.io/docs/launch/continuous-deployment-with-github-actions/)
