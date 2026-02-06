import pygame
import threading
from state_machine import State
from rule_sets import Classic
from cardpool import CardPool
from listener import Listener

class Init(State):
    def __init__(self):
        super().__init__()

        self.next = "GAME"
        self.listener = Listener()

        self.cardpool = CardPool()
        self.classic_constructor = Classic(self.cardpool)

        self.done = True

    def cleanup(self):
        self.persist['listener'] = self.listener
        self.persist['constructor'] = self.classic_constructor

        self.done = False
        return self.persist
