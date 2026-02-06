import pygame
from pathlib import Path
from state_machine import State
from rule_sets import Classic
from cardpool import CardPool
from card import Card

class Game(State):
    def __init__(self):
        State.__init__(self)
        self.player_id = 0
        self.pack_queue = []
        self.pack_ready = False

        self.cardpool = CardPool()
        self.classic_constructor = Classic(self.cardpool)
        self.current_pack = pygame.sprite.Group()
        self.current_player_packet = {}

    def startup(self, persistant):
        self.persist = persistant
        self.listener = self.persist['listener']

    def cleanup(self):
        self.done = False
        return self.persist

    def listen_for_data(self):
        if self.listener.data:
            unsorted_data = self.listener.data
            self.listener.data = None
            self.sort_data(unsorted_data)

    def sort_data(self, unsorted_data):
        if not self.player_id:
            self.player_id = unsorted_data['id']
            self.persist['player_id'] = self.player_id
        if unsorted_data['pack'] and not self.pack_queue[-1] == unsorted_data['pack']:
            self.pack_queue.append(unsorted_data['pack'])

    def construct_pack(self, constructor):
        pack = pygame.sprite.Group()
        dict_pack = constructor.construct_pack()

        for card_dict in dict_pack:
            pack.add(Card(card_dict))

        return pack

    def assemble_pack_from_id(self, constructor, id_pack):
        pack = pygame.sprite.Group()
        dict_pack = constructor.assemble_pack_from_id(id_pack)

        for card_dict in dict_pack:
            pack.add(Card(card_dict))

        return pack

    def construct_player_packet(self, pack):
        working = []
        for card in pack:
            working.append(card.id)

        return {'id': self.player_id, 'pack': working}

    def init_pack_check(self):
        if self.player_id and not self.current_player_packet and not self.pack_queue:
            self.current_pack = self.construct_pack(self.classic_constructor)
            self.current_player_packet = self.construct_player_packet(self.current_pack)
            self.pack_ready = True

        elif self.player_id and not self.current_player_packet:
            self.current_pack = self.assemble_pack_from_id(self.classic_constructor, self.pack_queue[0])
            self.pack_queue.pop(0)
            self.current_player_packet = self.construct_player_packet(self.current_pack)
            self.pack_ready = True

    def update(self, dt):
        self.listen_for_data()
        self.init_pack_check()
