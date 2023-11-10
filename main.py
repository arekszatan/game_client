import logging as log
from datetime import datetime
import socket
import time
import threading
from WebsocketClient import WebsocketClient


def ping_pong(cli_sock):
    while True:
        cli_sock.send("ping".encode())
        t = time.time()
        try:
            while True:
                data = cli_sock.recv(1024).decode()
                if data == "pong":
                    break
            print(round((time.time() - t)*1000, 2))
            time.sleep(1)
        except:
            print("Connection closed")
            break




def client_program():
    host = 'localhost'  # as both code is running on same pc
    port = 5001  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    t = threading.Thread(target=ping_pong, args=[client_socket])
    t.start()


if __name__ == "__main__":
    logName = datetime.today().strftime('%Y_%m_%d_logging.log')
    log.basicConfig(level=log.INFO, filename=logName, filemode='w',
                    format='%(asctime)s::%(levelname)s >>> %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
    log.info('Starting main game_client...')
    client = WebsocketClient()
    client.start()

