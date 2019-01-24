from enum import Enum

class Type(Enum):
    transformation = 0
    freeze = 1
    encasement = 2

class Duration(Enum):
    anyDuration = 0
    short = 1
    longDuration = 2
    extended = 3
    protracted = 4

class Settings:
    def __init__ (self, name = "Helpless Subject", duration = Duration.longDuration, permanenceChance = 0.1, stripChance = 0.4, maxArticles = 2, expressionChance = 0.3, poseChance = 0.3, transformationAllowed = True, freezeAllowed = True, encasementAllowed = False, blacklist = [], custom = [], helpless = False):
            vars(self).update((k,v) for k,v in vars().items() if k != 'self')

async def handle_set (client, message, name, channel, settings):
    words = message.content.split(None, 2)
    command = words[1].lower()
    if (len(words) < 3 or words[1] == "help"):
        await client.send_message(channel, 'Usage: !set <settingname> <value>\n' + \
         'Valid settings: name, duration, permanenceChance, stripChance, maxArticles, expressionChance, poseChance, transformationAllowed, freezeAllowed, encasementAllowed, blacklist, custom\n' + \
         'Choices for duration: a number 1-4 (short, long, extended, protracted) or 0 for random\n' + \
         'Choices for "chance" values: a number 0-100\n' + \
         'Choices for max articles: a number 0-6\n' + \
         'Choices for "allowed" values: t or f\n' + \
         'Choices for custom/blacklist: a comma-delimited string (or "none" to clear)')
        return
    if (command in ["name", "n"]):
        await client.send_message(channel, f'{settings.name}, your new name is **{words[2]}**')
        settings.name = words[2]
        return
    if (command in ["duration", "d"]):
        duration = get_duration(words[2])
        await client.send_message(channel, f'{settings.name}, your new duration setting is **{get_duration_description(duration)}**')
        settings.duration = duration
        return
    if (command in ["permanencechance", "pec"]):
        probability = probability_from_string(words[2])
        await client.send_message(channel, f'{settings.name}, your new chance of a permanent effect is **{probability}%**')
        settings.permanenceChance = probability / 100
        return            
    if (command in ["stripchance", "sc"]):
        probability = probability_from_string(words[2])
        await client.send_message(channel, f'{settings.name}, your new chance of being stripped is **{probability}%**')
        settings.stripChance = probability / 100
        return
    if (command in ["maxarticles", "ma"]):
        articles = clamp_max_articles(words[2])
        await client.send_message(channel, f'{settings.name}, your new maximum articles when being stripped is now **{articles}**')
        settings.maxArticles = articles
        return        
    if (command in ["expressionchance", "ec"]):
        probability = probability_from_string(words[2])
        await client.send_message(channel, f'{settings.name}, your new chance of being given an expression is **{probability}%**')
        settings.expressionChance = probability / 100
        return
    if (command in ["posechance", "pc"]):
        probability = probability_from_string(words[2])
        await client.send_message(channel, f'{settings.name}, your new chance of being posed is **{probability}%**')
        settings.poseChance = probability / 100
        return            
    if (command in ["transformationallowed", "ta"]):
        allowed = boolean_from_string(words[2])
        await client.send_message(channel, f'{settings.name}, your new setting for transfomation allowed is **{allowed}**')
        settings.transformationAllowed = allowed
        return      
    if (command in ["freezeallowed", "fa"]):
        allowed = boolean_from_string(words[2])
        await client.send_message(channel, f'{settings.name}, your new setting for freeze allowed is **{allowed}**')
        settings.freezeAllowed = allowed
        return      
    if (command in ["encasementallowed", "ea"]):
        allowed = boolean_from_string(words[2])
        await client.send_message(channel, f'{settings.name}, your new setting for encasement allowed is **{allowed}**')
        settings.encasementAllowed = allowed
        return
    if (command in ["custom", "c"]):
        custom = word_list_from_string(words[2])
        await client.send_message(channel, f'{settings.name}, your new custom material list is: **{custom}**')
        settings.custom = custom
        return              
    if (command in ["blacklist", "bl"]):
        blacklist = word_list_from_string(words[2])
        await client.send_message(channel, f'{settings.name}, your new material blacklist is: **{blacklist}**')
        settings.blacklist = blacklist
        return    

def probability_from_string(input: str) -> int:
    try:
        parsedInput = int(input)
    except:
        return -1
    if (parsedInput < 0):
        parsedInput = 0
    if (parsedInput > 100):
        parsedInput = 100
    return parsedInput
    
def clamp_max_articles(input: str) -> int:
    try:
        parsedInput = int(input)
    except:
        return 2
    if (parsedInput < 0):
        return 0
    if (parsedInput > 6):
        return 6
    return parsedInput

def get_duration(input: str) -> Duration:
    try:
        parsedInput = int(input)
    except:
        return Duration.longDuration
    if (parsedInput < 0 or parsedInput > 4):
        return Duration.longDuration
    return Duration(parsedInput)

def get_duration_description(duration: Duration) -> str:
    return ["random", "short", "long", "extended", "protracted"][duration.value]

def boolean_from_string(input: str) -> bool:
    if (input[0].lower() == 't'):
        return True
    return False

def word_list_from_string(input: str) -> list:
    strings = input.split(",")
    if (strings[0] == "none"):
        return []
    if (len(strings) > 10):
        strings = strings[:10]
    return [x.strip() for x in strings]


async def handle_view_settings (client, message, name, channel, settings):
    await client.send_message(channel, f'**{name}**, your settings are:\n')
    settings_string = f"""
**Name:** {settings.name}
**Helpless:** {settings.helpless}
**Duration:** {get_duration_description(settings.duration)}
**Permanence chance:** {settings.permanenceChance * 100}%
**Strip chance:** {settings.stripChance * 100}%
**Max articles:** {settings.maxArticles}
**Pose chance:** {settings.poseChance * 100}%
**Expression chance:** {settings.expressionChance * 100}%
**Transformation allowed:** {settings.transformationAllowed}
**Freeze allowed:** {settings.freezeAllowed}
**Encasement allowed:** {settings.encasementAllowed}
**Blacklist:** {settings.blacklist}
**Custom materials:** {settings.custom}
"""
    await client.send_message(channel, settings_string)    

async def handle_helpless (client, message, name, channel, settings):
    settings.helpless = not settings.helpless
    if (settings.helpless):
        await client.send_message(channel, f'**{name}** is now helpless!')
    else:
        await client.send_message(channel, f'**{name}** is no longer helpless.')
