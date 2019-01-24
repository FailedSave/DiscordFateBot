import discord
import asyncio

help_string = """ASFR Bot Commands:
**!fate**: Gives you a random ASFR effect
**!set <setting> <value>**: Choose settings for !fate
**!viewsettings**: View your current settings

All commands work over DM.
For support or suggestions, contact **FailedSave**.
Github: https://github.com/FailedSave/DiscordFateBot"""

async def handle_help (client, message, name, channel, settings):
    await client.send_message(channel, help_string)    
