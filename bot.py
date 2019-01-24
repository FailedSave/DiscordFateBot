import discord
import asyncio
import fate
from setting_storage import settings_from_user_id, target_settings_from_user_id
import setting_storage
import settings
import json
import help
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
    if message.content.startswith('!helpless'):
        await settings.handle_helpless(client, message, message.author.name, message.channel, settings_from_user_id(message.author))
    elif message.content.startswith('!h'):
        await help.handle_help(client, message, message.author.name, message.channel, settings_from_user_id(message.author))

    if message.content.startswith('!fate'):
        await fate.handle_fate(client, message, message.author.name, message.channel, settings_from_user_id(message.author))

    if message.content.startswith('!set'):
        await settings.handle_set(client, message, message.author.name, message.channel, settings_from_user_id(message.author))

    if message.content.startswith('!viewsettings'):
        await settings.handle_view_settings(client, message, message.author.name, message.channel, settings_from_user_id(message.author))

    if message.content.startswith('!tfate'):
        await fate.handle_target_fate(client, message, message.author.name, message.channel, target_settings_from_user_id(message.author))

    if message.content.startswith('!tset'):
        await settings.handle_set(client, message, message.author.name, message.channel, target_settings_from_user_id(message.author))

    if message.content.startswith('!tviewsettings'):
        await settings.handle_view_settings(client, message, message.author.name, message.channel, target_settings_from_user_id(message.author))

    if message.content.startswith('!save'):
        await setting_storage.save_settings()

    if message.content.startswith('!wfate'):
        await fate.handle_whisper_fate(client, message, message.author.name, message.channel, target_settings_from_user_id(message.author))

with open('.connections.json') as json_data:
    connections = json.load(json_data)

client.run(connections["MAIN"])