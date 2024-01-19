import socket
import sys
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
        self.running = True
        self.callback_obj = []
        log.info(f'Websocket client created')

    def run(self) -> None:
        log.info(f'Client started')
        t1 = threading.Thread(target=self.main)
        t1.start()
        while self.running:
            try:
                self.actual_callback_list = []
                self.actual_prefix_list = []
                self.client_socket = None
                self.recv_time = []
                log.info(f'Client trying connect to {HOST}, {PORT}')
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.settimeout(5)
                self.client_socket.connect((HOST, PORT))
                log.info(f'Client is connected to {HOST} and {PORT} [SUCCESS]')
                self.is_connected = True
                t2 = threading.Thread(target=self.pong)
                t2.start()
                t3 = threading.Thread(target=self.recv_message_from_server)
                t3.start()
                while True:
                    if not self.is_connected or not self.running:
                        break
                if not self.running:
                    t1.join()
                    t2.join()
                    t3.join()
            except Exception as e:
                log.exception(e)
                time.sleep(RECONNECT_TIME)
        sys.exit()

    def get_ping(self):
        if len(self.recv_time) == 0:
            return 0
        return round(sum(self.recv_time) / len(self.recv_time), 2)

    def pong(self):
        while self.running and self.is_connected:
            try:
                t = time.time()

                def callback_pong(message):
                    if PONG_LOG:
                        log.info(f'Get data from server {message}')
                    finish_time = round((time.time() - t) * 1000, 2)
                    self.recv_time.append(finish_time)
                    if len(self.recv_time) > 5:
                        self.recv_time.pop(0)
                self.send("ping", data="pong", callback=callback_pong)
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
        self.callback_obj.append(CallbackCommunication(method, callback, prefix, time.time()))
        try:
            self.client_socket.send(data.encode())
        except Exception as e:
            log.exception(e)
            self.is_connected = False

    def send(self, method="method", data="data", callback=None):
        t = threading.Thread(target=self.send_to_server, args=[method, data, callback])
        t.start()
        if not self.running:
            t.join()

    def recv_message_from_server(self):
        while self.running and self.is_connected:
            try:
                if not self.running:
                    break
                data_recv = self.client_socket.recv(1024).decode()
            except Exception as e:
                log.exception(e)
                break
            data_recv_format = f'[{data_recv.replace("}{", "},{")}]'
            json_object_list = json.loads(data_recv_format)
            for json_object in json_object_list:
                prefix_mess = json_object['prefix']
                callback_for_all = json_object['callback_for_all']
                message_callback = json_object['data']
                if callback_for_all is not None:
                    for callback in all_socket_callback:
                        if callback_for_all == callback.__name__:
                            callback(self, message_callback)
                            log.info(f'Callback for all {message_callback}')
                for obj in self.callback_obj:
                    if obj.get_prefix() == prefix_mess:
                        obj.proceed_callback(message_callback)
                        self.callback_obj.remove(obj)
            # print(self.callback_obj)
            for obj in self.callback_obj:
                if obj.get_time_exist() > 5:
                    self.callback_obj.remove(obj)


class CallbackCommunication:
    def __init__(self, method, callback, prefix, time_created):
        self.callback = callback
        self.prefix = prefix
        self.method = method
        self.time_created = time_created

    def get_time_exist(self):
        return time.time() - self.time_created

    def get_prefix(self):
        return self.prefix

    def get_callback(self):
        return self.callback

    def proceed_callback(self, param):
        if self.callback is None:
            return
        log.info(f'Callback {self.callback.__name__} for method {self.method} is proceeding')
        self.callback(param)
