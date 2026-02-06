from ..state_machine import State
from ..settings import HOST, PORT
import socket
import time
import pickle
import threading

class Connect(State):
    def __init__(self):
        super().__init__()
        self.host = HOST
        self.port = PORT

        self.kill = False

        self.player_id = 0

    def get_socket(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            s.connect((self.host, self.port))
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            s.settimeout(1)
            self.socket = s

    def run_listener(self, local_socket, deserialize, kill = None):
        while not kill:
            try:
                data = local_socket.recv(4096)
                if len(data):
                    deserialize(data)
            except socket.timeout or pickle.UnpicklingError:
                pass
            time.sleep(0.001)

    def deserialize(self, data):
        unsorted_data = pickle.loads(data)
        if not self.player_id:
            self.player_id = unsorted_data['id']

    def startup(self, persistant):
        self.persist = persistant
        self.get_socket()
        threading.Thread(target=self.run_listener, args=()).start()

    def update(self, dt):
        if self.player_id:
            self.done = True
            self.next = "GAME"

    def cleanup(self):
        self.done = False
        self.persist['socket'] = self.socket
        self.persist['player_id'] = self.player_id
        return self.persist
