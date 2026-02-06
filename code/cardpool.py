from update import get_json, write_json
from settings import CARD_POOL_FOLDER, CARD_POOL_JSON

class CardPool:
    def __init__(self):
        self.source_path = CARD_POOL_JSON
        self.card_list = get_json(self.source_path)

        self.destination_path = CARD_POOL_FOLDER
        self.destination_path.mkdir(parents=True, exist_ok=True)

        self.check_files()

    def check_files(self):
        file_list = ['nonlands.json', 'lands.json', 'commanders.json', 'super.json']

        self.nonland_path = self.destination_path / file_list[0]
        self.lands_path = self.destination_path / file_list[1]
        self.commanders_path = self.destination_path / file_list[2]
        self.super_path = self.destination_path / file_list[3]

        if not self.nonland_path.is_file():
            self.find_nonlands()
            write_json(self.nonland_path, self.nonlands)
        if not self.lands_path.is_file():
            self.find_lands()
            write_json(self.lands_path, self.lands)
        if not self.commanders_path.is_file():
            self.find_commanders()
            write_json(self.commanders_path, self.commanders)
        if not self.super_path.is_file():
            self.copy_super(self.super_path)

        if not hasattr(self, 'commanders'):
            self.nonlands = get_json(self.nonland_path)
            self.lands = get_json(self.lands_path)
            self.commanders = get_json(self.commanders_path)

    def copy_super(self, path):
        self.super = self.card_list
        write_json(path, self.super)

    def find_commanders(self):
        commanders = {}

        for key, card in self.card_list.items():
            has_oracle = None

            if "oracle_text" in card:
                has_oracle = True
            else:
                has_oracle = False

            if "Legendary" in card["type_line"] and "Creature" in card["type_line"]:
                commanders[key] = card
            elif has_oracle and "can be your commander" in card["oracle_text"]:
                commanders[key] = card

        self.commanders = commanders

    def find_lands(self):
        lands = {}

        for key, card in self.card_list.items():
            if "Land" in card['type_line']:
                lands[key] = card

        self.lands = lands

    def find_nonlands(self):
        nonlands = {}

        for key, card in self.card_list.items():
            if "Land" in card['type_line']:
                continue

            if 'oracle_text' in card:
                if 'TK' in card['oracle_text']:
                    continue

            if 'Attraction' in card['type_line']:
                continue

            nonlands[key] = card

        self.nonlands = nonlands

if __name__ == "__main__":
    cardpool = CardPool('commander', 'commander.json')
