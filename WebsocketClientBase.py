import socket
import threading
import logging as log
import time
from Settings import *
import random
import json
all_socket_callback = []


def socket_callback(func):
    all_socket_callback.append(func)


class WebsocketClientBase(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.recv_time = []
        self.client_socket = None
        self.is_connected = False
        self.actual_prefix_list = []
        self.actual_callback_list = []
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

    def get_ping(self):
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
        while True:
            index_list = []
            message_callback = None
            message_list = []
            callback_for_all = None
            while True:
                data_recv = self.client_socket.recv(1024).decode()
                data_recv_format = data_recv.replace('}{', '},{')
                data_recv_format = f'[{data_recv_format}]'
                json_object_list = json.loads(data_recv_format)
                for json_object in json_object_list:
                    prefix_mess = json_object['prefix']
                    callback_for_all = json_object['callback_for_all']
                    if callback_for_all is not None:
                        message_callback = json_object['data']
                        continue
                    message_list.append(json_object['data'])
                    if int(prefix_mess) in self.actual_prefix_list:
                        index = self.actual_prefix_list.index(prefix_mess)
                        index_list.append(index)
                break
            index_offset = 0
            for index in index_list:
                if self.actual_callback_list[index - index_offset] is not None:
                    self.actual_callback_list[index - index_offset](message_list[index - index_offset])
                self.actual_callback_list.pop(index - index_offset)
                self.actual_prefix_list.pop(index - index_offset)
                message_list.pop(index - index_offset)
                index_offset += 1

            if callback_for_all is not None:
                #print(all_socket_callback)
                for callback in all_socket_callback:
                    if callback_for_all == callback.__name__:
                        callback(self, message_callback)
                        log.info(f'Callback for all {message_callback}')

