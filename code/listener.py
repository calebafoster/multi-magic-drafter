from settings import HOST, PORT
import socket
import time
import pickle

class Listener:
    def __init__(self):
        self.host = HOST
        self.port = PORT

        self.kill = False

        self.get_socket()

    def get_socket(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            s.connect((self.host, self.port))
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            s.settimeout(1)
            self.socket = s

    def run_listener(self):
        while not self.kill:
            try:
                data = self.socket.recv(4096)
                if len(data):
                    self.data = self.deserialize(data)
            except socket.timeout or pickle.UnpicklingError:
                pass
            time.sleep(0.001)

    def deserialize(self, data):
        return pickle.loads(data)

    def serialize(self, data):
        pass
