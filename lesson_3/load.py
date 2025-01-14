import json
import os

USERS_FILE = 'users.json'
PLAY_FILE = 'play.json'

def load_questions():
    if os.path.exists(PLAY_FILE):
        with open(PLAY_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def load():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

users = load()