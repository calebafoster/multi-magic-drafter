import random
from update import get_json

class Classic:
    def __init__(self, cardpool):
        self.cardpool = cardpool

    def construct_pack(self, num = 7):

        keys_list = list(self.cardpool.commanders.keys())
        random.shuffle(keys_list)
        commander = self.cardpool.commanders[keys_list[0]]
        keys_list = list(self.cardpool.lands.keys())
        random.shuffle(keys_list)
        land = self.cardpool.lands[keys_list[0]]

        pack = [commander, land]

        keys_list = list(self.cardpool.nonlands.keys())
        print(keys_list)
        random.shuffle(keys_list)
        for i in range(num - len(pack)):
            pack.append(self.cardpool.nonlands[keys_list[i]])

        return pack

    def assemble_pack_from_id(self, id_pack):
        pack = []
        for id in id_pack:
            card_dict = self.cardpool.super[id]
            pack.append(card_dict)

        return pack
