import socket
import threading
import logging as log
import time
from Settings import *
import random
import json


class WebsocketClientBase(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = bool
        self.connected = []
        self.recv_time = []
        self.client_socket = None
        self.is_connected = False
        self.actual_prefix_list = []
        self.actual_callback_list = []
        self.a = 0
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
                t = threading.Thread(target=self.recv_message_from_server)
                t.start()
                while self.is_connected:
                    try:
                        self.main()
                    except Exception as e:
                        log.exception(e)
                        break
            except Exception as e:
                log.exception(e)
                time.sleep(RECONNECT_TIME)

    def get_ping(self) -> int:
        if len(self.recv_time) == 0:
            return 0
        return round(sum(self.recv_time) / len(self.recv_time), 2)

    def pong(self):
        while True:
            try:
                t = time.time()

                def callback_pong(message):
                    if PONG_LOG:
                        log.info(f'Get data from server {message}')
                    finish_time = round((time.time() - t) * 1000, 2)
                    self.recv_time.append(finish_time)
                    if len(self.recv_time) > 5:
                        self.recv_time.pop(0)
                self.send_to_server("ping", data="pong", callback=callback_pong)
                time.sleep(3)
            except Exception as e:
                log.exception(e)
                self.is_connected = False
                if self.client_socket:
                    self.client_socket.close()
                break

    def main(self):
        ...

    def send_to_server(self, method="method", data="data", callback=None):
        prefix = random.randint(100000, 999999)
        data = {
            "prefix": prefix,
            "method": method,
            "data": data
        }
        data = json.dumps(data)
        self.actual_prefix_list.append(prefix)
        self.actual_callback_list.append(callback)
        self.client_socket.send(data.encode())


    def send(self, method="method", data="data", callback=None):
        t = threading.Thread(target=self.send_to_server, args=[method, data, callback])
        t.start()

    def recv_message_from_server(self):
        index_list = []
        message_list = []
        i = 0
        a = 0
        while True:
            while True:
                data_recv = self.client_socket.recv(1024).decode()
                #print(data_recv)
                data_recv_format = data_recv.replace('}{', '},{')
                data_recv_format = f'[{data_recv_format}]'
                json_object_list = json.loads(data_recv_format)
                #print(json_object_list)
                for json_object in json_object_list:
                    i += 1
                    #print(json_object, )
                    #print(json_object)
                    #json_object = json.loads(json_object)
                    prefix_mess = json_object['prefix']
                    #message = json_object['data']
                    message_list.append(json_object['data'])
                    #print(prefix_mess, self.actual_prefix_list)
                    if int(prefix_mess) in self.actual_prefix_list:
                        a += 1
                        index = self.actual_prefix_list.index(prefix_mess)
                        index_list.append(index)
                break
            a = 0
            for index in index_list:
                #print(self.actual_callback_list, index - a)
                #print(self.actual_callback_list, index_list)
                if self.actual_callback_list[index - a] is not None:
                    self.actual_callback_list[index - a](message_list[index - a])
                self.actual_callback_list.pop(index - a)
                self.actual_prefix_list.pop(index - a)
                message_list.pop(index - a)
                a += 1

            index_list = []
            #print(i, a)
