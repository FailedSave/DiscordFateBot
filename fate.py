from settings import Settings, Type
from setting_storage import find_settings_from_name
import discord
import asyncio
import random
import json

delay = 0.9

async def handle_fate(client, message, name, channel, settings):
    await client.send_message(channel, f'**{settings.name}**, your fate is...')
    await asyncio.sleep(delay)

    for string in get_fate_strings(settings):
        await client.send_message(channel, string)
        await asyncio.sleep(delay)

async def handle_target_fate(client, message, name, channel, settings):
    words = message.content.split(None, 1)
    if len(words) < 2:
        await client.send_message(channel, f"This command needs a target.")
    target_name = words[1]

    target_settings = find_settings_from_name(target_name)
    if target_settings is None:
        await client.send_message(channel, f"**{target_name}** not found. (Have they ever interacted with me?)")
        return
    elif not target_settings.helpless:
        await client.send_message(channel, f"**{target_name}** is not helpless!")
        return

    await client.send_message(channel, f'**{target_name}**, **{message.author.name}** has decided that your fate is...')
    await asyncio.sleep(delay)

    for string in get_fate_strings(settings):
        await client.send_message(channel, string)
        await asyncio.sleep(delay)

async def handle_whisper_fate(client, message, name, channel, settings):
    words = message.content.split(None, 1)
    target_name = words[1]

    target_settings = find_settings_from_name(target_name)
    if target_settings is None:
        await client.send_message(channel, f"**{target_name}** not found. (Have they ever interacted with me?)")
        return
    elif not target_settings.helpless:
        await client.send_message(channel, f"**{target_name}** is not helpless!")
        return

    target_fate = get_fate_strings(settings)

    await client.send_message(target_settings.user, f'**{target_name}**, **{message.author.name}** has decided that your fate is...')
    target_fate_string = f"**{target_name}'s** fate is...\n"
    await asyncio.sleep(delay)

    for string in target_fate:
        await client.send_message(target_settings.user, string)
        await asyncio.sleep(delay)
        target_fate_string = target_fate_string + string + "\n"

    await client.send_message(message.author, target_fate_string)    

def get_fate_strings(settings: Settings) -> list:
    strings = []
    if (check_probability(settings.stripChance)):
        strings.append(get_message_for_strip(settings))

    type_and_material = get_type_and_material(settings)
    strings.append(get_message_for_type_and_material(type_and_material))

    if (check_probability(settings.expressionChance)):
        strings.append(get_message_for_expression(type_and_material["effectType"]))

    if (check_probability(settings.poseChance)):
        strings.append(get_message_for_pose(settings))

    strings.append(get_duration_message(settings))
    return strings
    

with open('data.json') as json_data:
    d = json.load(json_data)
    poseList = d["poseList"]
    transformationMaterialsList = d["transformationMaterialsList"]
    freezeMaterialsList = d["freezeMaterialsList"]
    encasementMaterialsList = d["encasementMaterialsList"]
    transformationExpressionList = d["transformationExpressionList"]
    freezeExpressionList = d["freezeExpressionList"]
    encasementExpressionList = d["encasementExpressionList"]
    durationsListOfLists = [d["shortDurationList"], d["longDurationList"], d["extendedDurationList"], d["protractedDurationList"]]

def get_type_and_material(settings: Settings):
    allowedTypes = []
    if (settings.transformationAllowed):
        allowedTypes.append(Type.transformation)
    if (settings.freezeAllowed):
        allowedTypes.append(Type.freeze)
    if (settings.encasementAllowed):
        allowedTypes.append(Type.encasement)
    if (len(allowedTypes)) == 0:
        allowedTypes.append(Type.transformation)
    
    allowed_materials = []
    effectType = random.choice(allowedTypes)
    if (effectType == Type.transformation):
        allowed_materials.extend(transformationMaterialsList)
    if (effectType == Type.freeze):
        allowed_materials.extend(freezeMaterialsList)
    if (effectType == Type.encasement):
        allowed_materials.extend(encasementMaterialsList)

    allowed_materials = [material for material in allowed_materials if does_not_contain_any(material, settings.blacklist)]
    for item in settings.custom:
        allowed_materials.append(item)

    return {"effectType": effectType, "material": random.choice(allowed_materials)}

def does_not_contain_any(input: str, blacklist: list):
    for item in blacklist:
        if (input.find(item) >= 0):
            return False
    return True

def check_probability(chance) -> bool:
    return random.random() < chance

def get_message_for_strip(settings) -> str:
    articles = random.randint(0, settings.maxArticles)
    if (articles == 0):
        return "You will be stripped **completely naked**..."
    elif (articles == 1):
        return "You will be stripped **down to 1 article of clothing**..."
    else:
        return f"You will be stripped **down to {articles} articles of clothing**..."

def get_message_for_pose(settings) -> str:
    return f"...you are posed {random.choice(poseList)}..."

def get_message_for_expression(effectType) -> str:
    expressionChoices = ["invalid effect type"]
    if (effectType == Type.transformation):
        expressionChoices = transformationExpressionList
    elif (effectType == Type.freeze):
        expressionChoices = freezeExpressionList
    elif (effectType == Type.encasement):
        expressionChoices = encasementExpressionList

    return f"...{random.choice(expressionChoices)}..."

def get_message_for_type_and_material(type_and_material) -> str:
    effectType = type_and_material["effectType"]
    material = type_and_material["material"]
    if (effectType == Type.transformation):
        return f'You will be turned into **{material}**...'
    elif (effectType == Type.freeze):
        return f'You will be **{material}**...'
    elif (effectType == Type.encasement):
        return f'You will be encased in **{material}**...'
    else:
        return f'Error: invalid effect type'

def get_duration_message(settings) -> str:
    if (check_probability(settings.permanenceChance)):
        return "...you will stay that way **permanently!**"
    duration = settings.duration.value
    if (duration == 0):
        duration = random.randint(1, 4)
    time = random.choice(durationsListOfLists[duration - 1])
    return f"...you will stay that way for the next **{time}**."     

