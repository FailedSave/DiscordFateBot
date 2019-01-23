import discord
import asyncio
import fate
from setting_storage import settings_from_user_id
import setting_storage
import settings
import json
from settings import Settings

client = discord.Client()




@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    setting_storage.load_settings()

@client.event
async def on_message(message):
    if message.content.startswith('!fate'):
        await fate.handle_fate(client, message, message.author.name, message.channel, settings_from_user_id(message.author))

    if message.content.startswith('!set'):
        await settings.handle_set(client, message, message.author.name, message.channel, settings_from_user_id(message.author))

    if message.content.startswith('!viewsettings'):
        await settings.handle_view_settings(client, message, message.author.name, message.channel, settings_from_user_id(message.author))

    if message.content.startswith('!save'):
        await setting_storage.save_settings()

    if message.content.startswith('!whisperfate'):
        if len(message.mentions) > 0:
            await fate.handle_fate(client, message, message.mentions[0].name, message.mentions[0], Settings())
        else:
            await fate.handle_fate(client, message, message.author.name, message.author, Settings())


    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

with open('.connections.json') as json_data:
    connections = json.load(json_data)

client.run(connections["TEST"])