import json
import os


PLAY_FILE = 'play.json'

def load_questions():
    if os.path.exists(PLAY_FILE):
        with open(PLAY_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}
