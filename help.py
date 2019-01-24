import discord
import asyncio

help_string = """ASFR Bot Commands:
**!fate**: Gives you a random ASFR effect
**!set <setting> <value>**: Choose settings for !fate
**!viewsettings**: View your current settings
**!helpless**: Toggles ability to be targeted by other users
**!tfate <target>**: Gives the target a random ASFR effect if helpless
**!tset <setting> <value>**: Choose settings for !tfate for your target
**!tviewsettings**: View your current !tfate settings

All commands work over DM.
For support or suggestions, contact **FailedSave**.
Github: https://github.com/FailedSave/DiscordFateBot"""

async def handle_help (client, message, name, channel, settings):
    await client.send_message(channel, help_string)    
