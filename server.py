import pickle
import socket
import time
import threading

# deserialize takes additional data and interprets the result to determine what it does
# f -> first time connection

class Server:
    def __init__(self, host="127.0.0.1", port=55885):
        self.host = host
        self.port = port

        self.kill = False
        self.thread_count = 0

        self.next_id = 1
        self.unsorted_data = None
        self.data_to_send = None

        self.player_collection = []
        self.player_map = {}
        self.current_pack = []

    def add_player(self, connection):
        player_dict = {}
        player_id = self.next_id
        self.next_id += 1

        player_dict = {'id': player_id, 'pack': []}
        self.player_collection.append(player_dict)
        self.player_map[player_id] = connection
        connection.send(pickle.dumps(player_dict))
        print("sent: " + str(player_dict))

    def serialize(self):
        pass

    def deserialize(self, data):
        decoded_data = pickle.loads(data)
        self.unsorted_data = decoded_data

    def run_listener(self, conn):
        self.thread_count += 1

        conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        conn.settimeout(1)

        while not self.kill:
            try:
                data = conn.recv(4096)
                if len(data):
                    self.deserialize(data)
            except socket.timeout:
                pass

        self.thread_count -= 1

    def connection_listen_loop(self):
        self.thread_count += 1

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            s.bind((self.host, self.port))

            while not self.kill:
                s.settimeout(1)
                s.listen()

                try:
                    conn, addr = s.accept()
                    print(conn, addr)
                    self.add_player(conn)
                    threading.Thread(target=self.run_listener,args=(conn,)).start()
                except socket.timeout:
                    continue

            time.sleep(0.01)

        self.thread_count -= 1

    def await_kill(self):
        self.kill = True
        while self.thread_count:
            time.sleep(0.01)

    def sort_data(self):
        if self.unsorted_data:
            id = self.unsorted_data['id']
            pack = self.unsorted_data['pack']

            for index, player in enumerate(self.player_collection):
                if id == player['id']:
                    self.player_collection[index]['pack'] = pack

            self.unsorted_data = None

    def send_data(self):
        if self.data_to_send:
            player_id = self.data_to_send['id']
            connection = self.player_map[player_id]
            connection.send(pickle.dumps(self.data_to_send))

            self.data_to_send = None

    def run(self):
        threading.Thread(target=self.connection_listen_loop).start()

        try:
            while(True):
                self.sort_data()
                self.send_data()
        except KeyboardInterrupt:
            self.await_kill()

Server().run()
