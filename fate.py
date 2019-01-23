from settings import Settings
from settings import Type
import discord
import asyncio
import random
import json

delay = 0.9

async def handle_fate(client, message, name, channel, settings):
    if (message.author.name == name):
        await client.send_message(channel, f'**{name}**, your fate is...')
    else:
        await client.send_message(channel, f'**{name}**, **{message.author.name}** has decided that your fate is...')
    await asyncio.sleep(delay)

    if (check_probability(settings.stripChance)):
        await client.send_message(channel, get_message_for_strip(settings))
        await asyncio.sleep(delay)

    type_and_material = get_type_and_material(settings)
    await client.send_message(channel, get_message_for_type_and_material(type_and_material))
    await asyncio.sleep(delay)

    if (check_probability(settings.expressionChance)):
        await client.send_message(channel, get_message_for_expression(type_and_material["effectType"]))
        await asyncio.sleep(delay)

    if (check_probability(settings.poseChance)):
        await client.send_message(channel, get_message_for_pose(settings))
        await asyncio.sleep(delay)

    await client.send_message(channel, f'{get_duration_message(settings)}')

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

