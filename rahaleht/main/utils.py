import json
import os

default_lang = "et"

def get_lang(lang, page, text):
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(current_dir, "static", "lang.json")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get(lang, {}).get(page, {}).get(text, text)