import json


def load_config():
    with open("config.json", "r", encoding="utf-8") as cfg:
        data = json.load(cfg)
        return data
