import logging as log
from datetime import datetime
import socket
import time

def client_program():
    host = 'localhost'  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        t = time.time()
        data = client_socket.recv(1024).decode()  # receive response
        print(round(time.time()-t, 2))
        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == "__main__":
    logName = datetime.today().strftime('%Y_%m_%d_logging.log')
    log.basicConfig(level=log.INFO, filename=logName, filemode='w',
                    format='%(asctime)s::%(levelname)s >>> %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
    log.info('Starting main game_client...')
    client_program()

import asyncio

# import websocket
# # websocket.enableTrace(True)
# def on_open(wsapp):
#     wsapp.send("Hello")
#
# def on_message(ws, message):
#     print(message)
#     ws.send("Send a ping", websocket.ABNF.OPCODE_PING)
#
# def on_pong(wsapp, message):
#     print(message)
#     print("Got a pong! No need to respond")
#     # wsapp.send("Send a ping", websocket.ABNF.OPCODE_PING)
# wsapp = websocket.WebSocketApp("ws://127.0.0.1:8765", on_open=on_open, on_message=on_message, on_pong=on_pong)
# wsapp.run_forever()