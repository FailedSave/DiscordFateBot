from settings import Settings
from settings import Type
import pickle
import os

settings_dict = {}
target_settings_dict = {}

def settings_from_user_id(user) -> Settings:
    if (user.id not in settings_dict):
        settings_dict[user.id] = Settings()
        settings_dict[user.id].name = user.name
        settings_dict[user.id].user = user
    return settings_dict[user.id]

def target_settings_from_user_id(user) -> Settings:
    if (user.id not in target_settings_dict):
        target_settings_dict[user.id] = Settings()
        target_settings_dict[user.id].name = user.name
    return target_settings_dict[user.id]

def find_settings_from_name(name) -> Settings:
    for settings in settings_dict.values():
        if settings.name.lower() == name.lower():
            return settings
    return None

async def save_settings():
    output = open('settings.pkl', 'wb')

    pickle.dump((settings_dict, target_settings_dict), output)
    output.close()

def load_settings():
    global settings_dict
    global target_settings_dict
    if (os.path.isfile('settings.pkl')):
        input = open('settings.pkl', 'rb')
        (settings_dict, target_settings_dict) = pickle.load(input)
        input.close()
    else:
        settings_dict = {}
        target_settings_dict = {}
