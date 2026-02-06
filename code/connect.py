from state_machine import State
from threading import Thread
import time

class Connect(State):
    def __init__(self):
        super().__init__()
        
    def startup(self, persistant):
        self.persist = persistant
        self.listener = self.persist['listener']
        try:
            Thread(target=self.listener.run_listener).start()
        except:
            print("CONNECTION REFUSED")

            print(self.previous)

    def update(self, dt):
        self.next = self.previous
        self.done = True
