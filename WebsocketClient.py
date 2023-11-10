import socket
import threading
import logging as log
import time
from Settings import *
import random
import json


class WebsocketClient(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = bool
        self.connected = []
        self.recv_time = []
        self.client_socket = None
        self.is_connected = False
        log.info(f'Websocket client created')

    def run(self) -> None:
        log.info(f'Client started')
        while True:
            try:
                log.info(f'Client trying connect to {HOST}, {PORT}')
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((HOST, PORT))
                log.info(f'Client is connected to {HOST} and {PORT} [SUCCESS]')
                self.is_connected = True
                t = threading.Thread(target=self.pong)
                t.start()
                i = 0
                while self.is_connected:
                    try:
                        self.test()
                    except Exception as e:
                        log.exception(e)
                        break
            except Exception as e:
                log.exception(e)
                time.sleep(3)

    def send_to_server(self, method, data="data"):
        prefix = self.get_prefix()
        data = {
            "prefix": prefix,
            "method": method,
            "data": data
        }
        data = json.dumps(data)
        self.client_socket.send(data.encode())
        while True:
            data_recv = self.client_socket.recv(1024).decode()
            json_object = json.loads(data_recv)
            prefix_mess = json_object['prefix']
            message = json_object['data']
            if prefix == int(prefix_mess):
                return message

    def get_ping(self):
        if len(self.recv_time) == 0:
            return 0
        return round(sum(self.recv_time)/len(self.recv_time), 2)

    def get_prefix(self):
        return random.randint(100000, 999999)

    def pong(self):
        while True:
            try:
                t = time.time()
                message = self.send_to_server("ping")
                if PONG_LOG:
                    log.info(f'Get data from server {message}')
                finish_time = round((time.time() - t) * 1000, 2)
                self.recv_time.append(finish_time)
                if len(self.recv_time) > 5:
                    self.recv_time.pop(0)
                time.sleep(3)
            except Exception as e:
                log.exception(e)
                self.is_connected = False
                if self.client_socket:
                    self.client_socket.close()
                break

    def test(self):
        input("Get oponent pres any key")
        wynik = self.send_to_server("test")
        print(wynik)

        # input("Get oponent pres any key")
        # prefix = self.get_prefix()
        # data = {
        #     "prefix": prefix,
        #     "method": "test",
        #     "data": "add_player"
        # }
        # data = json.dumps(data)
        # self.client_socket.send(data.encode())
        # while True:
        #     data_recv = self.client_socket.recv(1024).decode()
        #     json_object = json.loads(data_recv)
        #     prefix_mess = json_object['prefix']
        #     message = json_object['data']
        #     if prefix == int(prefix_mess):
        #         print(message)
        #         break
