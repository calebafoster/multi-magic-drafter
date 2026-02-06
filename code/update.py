import requests
import json
from pathlib import Path

oracle_path = Path('oracle-cards.json')
commander_path = Path('commander.json')

def download_oracle_cards():
    r = requests.get('https://api.scryfall.com/bulk-data')
    
    download_uri = r.json()['data'][0]['download_uri']

    r = requests.get(download_uri)

    oracle_cards = r.json()

    oracle_dict = {}

    for card in oracle_cards:
        card_id = card['id']
        oracle_dict[card_id] = card

    write_json(oracle_path, oracle_dict)

def commander_legal_list():
    oracle_dict = get_json(oracle_path)

    legals = {}
    for key, card in oracle_dict.items():
        if card["legalities"]["commander"] == "legal":
            legals[key] = card

    return legals

def update():
    download_oracle_cards()

    if oracle_path.is_file() and not commander_path.is_file():
        write_json(commander_path, commander_legal_list())

def get_json(path):
    with open(path, 'r', encoding="utf8") as f:
        file = json.load(f)
        return file

def write_json(path, obj_list):
    with open(path, 'w', encoding="utf8") as f:
        json.dump(obj_list, f, indent=4)

if __name__ == '__main__':
    update()
