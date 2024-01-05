import inspect
import threading
import time
import pygame
import sys
from WebsocketClientBase import WebsocketClientBase, socket_callback
from Settings import *
from GamePygame import GamePygame


class GameClient(WebsocketClientBase):
    def __init__(self):
        super().__init__()
        self.game = None

    def main(self):
        while True:
            if self.game is None:
                self.game = GamePygame(self)
            self.game.start_game()
            if not self.running:
                break
    def position_after_move(self, player_x):
        self.send(method="position_after_move", data=player_x, callback=None)

    @socket_callback
    def set_players_position(self, callback_mess):
        self.game.set_enemy_position(int(callback_mess))
