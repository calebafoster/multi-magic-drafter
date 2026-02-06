import pygame
import pickle
import threading
import socket
import time
import sys
import json
import random
from update import get_json, write_json
from cardpool import CardPool
from card import Card
from pathlib import Path
from rule_sets import Classic
from state_machine import StateMachine
from .states import game, connect

# idea for powerups: click on card to guarantee color identity match
# as well as click to reroll or block cards for the next person to take

STATE_DICT = {
        "GAME": game.Game(),
        "CONNECT": connect.Connect()
        }

class Main:
    def __init__(self, host = "127.0.0.1", port = 55885):
        pygame.init()
        self.display_surface = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Ethan's Birthday Game 2")
        self.clock = pygame.time.Clock()

        self.state_machine = StateMachine()
        self.state_machine.setup_states(STATE_DICT, "CONNECT")
        self.state_machine.state.startup({})

        self.host = host
        self.port = port
        self.kill = False
        self.socket = None

        self.player_id = 0
        self.pack_queue = []
        self.pack_ready = False

        self.cardpool = CardPool('commander', Path('commander.json'))
        self.classic_constructor = Classic(self.cardpool)

        self.current_pack = pygame.sprite.Group()
        self.current_player_pack = {}

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

    def construct_player_pack(self, pack):
        working = []
        for card in pack:
            working.append(card.id)

        return {'id': self.player_id, 'pack': working}

    def run_listener(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            s.connect((self.host, self.port))
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            s.settimeout(1)
            self.socket = s
            
            while not self.kill:
                try:
                    data = self.socket.recv(4096)
                    if len(data):
                        self.deserialize(data)
                except socket.timeout or pickle.UnpicklingError:
                    pass
                time.sleep(0.001)

    def serialize(self, data):
        return pickle.dumps(data)

    def deserialize(self, data):
        unsorted_data = pickle.loads(data)
        if not self.player_id:
            self.player_id = unsorted_data['id']

        if unsorted_data['pack']:
            self.pack_queue.append(unsorted_data['pack'])
            print(self.pack_queue)

    def send_data(self):
        try:
            if self.socket and self.pack_ready:
                self.socket.sendall(self.serialize(self.current_player_pack))
                self.pack_ready = False
        except OSError:
            pass

    def run(self):
        threading.Thread(target=self.run_listener).start()
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.kill = True
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick(120) / 1000

            if self.player_id and not self.current_player_pack:
                self.current_pack = self.construct_pack(self.classic_constructor)
                self.current_player_pack = self.construct_player_pack(self.current_pack)
                self.pack_ready = True

            self.send_data()
            self.state_machine.state.update(dt)
            self.state_machine.state.draw(self.display_surface)

            self.display_surface.fill('black')

            pygame.display.update()

if __name__ == "__main__":
    Main().run()
