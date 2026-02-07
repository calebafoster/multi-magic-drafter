import pygame
from state_machine import State
from card import Card
from settings import CARD_DIMENSIONS, SURFACE_CENTER

# First the game needs to detect initial connection and create the first pack
# Second the game needs to pick a card and send the pack off to the server with the card missing
# Third the game recieves a new pack from the server and assembles it. If the pack has one card, don't send the pack. Instead create a new pack
# loop through 2 and 3

class Game(State):
    def __init__(self):
        State.__init__(self)
        self.player_id = 0
        self.pack_queue = []

        self.packet_ready = False

        self.new_pack_bool = False

        self.construct_ready = True
        self.assemble_ready = False

        self.can_space = True
        self.can_cycle = True

        self.tape_index = 0

        self.current_pack = pygame.sprite.Group()
        self.tape_cards = pygame.sprite.Group()
        self.current_player_packet = {}

    def startup(self, persistant):
        self.persist = persistant
        self.listener = self.persist['listener']
        self.constructor = self.persist['constructor']

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

    def connect_temp_hotkey(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_space:
            self.done = True
            self.can_space = False
            self.next = 'CONNECT'

    def new_pack_logic(self):
        if self.new_pack_bool:
            self.current_pack = self.construct_pack(self.constructor)
            self.new_pack_bool = False

        if not self.current_pack and self.player_id:
            self.new_pack_bool = True

    def send_player_packet(self):
        if self.packet_ready:
            self.packet_ready = False
            data_to_send = self.listener.serialize(self.current_player_packet)
            self.listener.socket.sendall(data_to_send)

    def arrange_tape(self):
        self.tape_cards.empty()

        if not self.current_pack:
            return 0

        adjusted_tape_index = self.tape_index % len(self.current_pack)
        selected_card = self.current_pack.sprites()[adjusted_tape_index]
        selected_card.rect.center = SURFACE_CENTER

        for index, card in enumerate(self.current_pack.sprites()):
            relative_index = index - adjusted_tape_index

            card.rect.center = selected_card.rect.center
            card.rect.x += relative_index * CARD_DIMENSIONS.x
            self.tape_cards.add(card)

    def cycle_tape_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.can_cycle:
            self.can_cycle = False
            self.tape_index -= 1
            self.arrange_tape()

        if keys[pygame.K_RIGHT] and self.can_cycle:
            self.can_cycle = False
            self.tape_index += 1
            self.arrange_tape()

        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.can_cycle = True

    def update(self, dt):
        self.connect_temp_hotkey()
        self.cycle_tape_input()
        self.listen_for_data()
        self.send_player_packet()
        self.new_pack_logic()

    def draw(self, surface):
        self.tape_cards.draw(surface)
