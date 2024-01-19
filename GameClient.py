from WebsocketClientBase import WebsocketClientBase, socket_callback
from GamePygame import GamePygame


class GameClient(WebsocketClientBase):
    def __init__(self):
        super().__init__()
        self.game = None
        self.is_connected_with_room = False
        self.room_name = ""
        self.my_name_room = "NoName"
        self.enemy_name_room = "-"
        self.is_start_window = True
        self.game_is_ready = False

    def main(self):
        while True:
            if self.game is None:
                self.game = GamePygame(self)
            self.game.start_game()
            if not self.running:
                break

    def position_after_move(self, player_x):
        self.send(method="position_after_move", data=player_x, callback=self.position_after_move_callback)

    def position_after_move_callback(self, data):
        if data is None:
            return
        self.game.player_x = int(data)

    def connect_with_game_room(self):
        if self.is_connected_with_room:
            return
        self.send(method="connect_with_game_room", data=self.my_name_room,
                  callback=self.connect_with_game_room_callback)

    def connect_with_game_room_callback(self, data):
        if data is None:
            return
        self.is_connected_with_room = True
        self.room_name = data['name_room']
        self.enemy_name_room = data['player_1']
        self.game_is_ready = True

    def create_game_room(self):
        if self.is_connected_with_room:
            return
        self.send(method="create_game_room", data=self.my_name_room,
                  callback=self.create_game_room_callback)

    def create_game_room_callback(self, data):
        if data is None:
            return
        self.room_name = str(data)
        self.is_connected_with_room = True

    @socket_callback
    def set_enemy_position(self, callback_mess):
        self.game.set_enemy_position(int(callback_mess))

    @socket_callback
    def set_player_name(self, callback_mess):
        self.enemy_name_room = callback_mess
        self.game_is_ready = True

    @socket_callback
    def set_enemy_bullets(self, callback_mess):
        self.game.set_enemy_bullets(callback_mess)

    @socket_callback
    def send_score(self, callback_mess):
        self.game.score = callback_mess
