from settings import Settings
from settings import Type
import pickle
import os

settings_dict = {}

def settings_from_user_id(user) -> Settings:
    if (user.id not in settings_dict):
        settings_dict[user.id] = Settings()
        settings_dict[user.id].name = user.name
    return settings_dict[user.id]

async def save_settings():
    output = open('settings.pkl', 'wb')

    pickle.dump(settings_dict, output)
    output.close()

def load_settings():
    global settings_dict
    if (os.path.isfile('settings.pkl')):
        input = open('settings.pkl', 'rb')
        settings_dict = pickle.load(input)
        input.close()
    else:
        settings_dict = {}
