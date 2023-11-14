import time
from WebsocketClientBase import WebsocketClientBase


class GameClient(WebsocketClientBase):
    def __init__(self):
        super().__init__()

    def main(self):
        # self.test()
        pass

    def test(self):
        input("Get oponent pres any key")
        self.send(method="test", data="", callback=self.call_test)
        print("Waiting for other player")
        while True:
            # wynik = self.send_to_server(method="test1", data="")
            # if wynik:
            #     break
            time.sleep(1)
        print("start gry")

    def call_test(self, callback_mess):
        print("i am call back", callback_mess)