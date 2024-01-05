import pygame
from Settings import *
import threading
from Button import Button, buttons_update


class GamePygame:
    def __init__(self, parent):
        self.parent = parent
        pygame.init()
        self.game_width, self.game_height = 700, 650
        self.game_screen = pygame.display.set_mode((self.game_width, self.game_height))
        self.clock = pygame.time.Clock()
        self.font36 = pygame.font.Font(pygame.font.get_default_font(), 36)
        self.font20 = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.running = True
        self.is_start_game = True
        self.player_speed = 5
        self.player_size = 50
        self.player_x = 80
        self.enemy_x = 60
        self.__item_define()

    def start_game(self):
        self.__main()

    def __main(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.parent.running = False
                pygame.quit()
                return
        if self.is_start_game:
            self.start_window()
            buttons_update()
        else:
            self.game_window()
            self.check_game_event()
        pygame.display.flip()
        self.clock.tick(TIC)

    def __item_define(self):
        Button(self.game_screen, "Start Game", 300, 300, 100, 50, self.start_button_clicked)

    def check_game_event(self):
        pygame.display.set_caption("ASZA GAME")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player_x > 0:
            self.player_x -= self.player_speed
            self.parent.position_after_move(self.player_x)
        if keys[pygame.K_RIGHT] and self.player_x < self.game_width - self.player_size:
            self.player_x += self.player_speed
            self.parent.position_after_move(self.player_x)

    def start_window(self):
        self.game_screen.fill(WHITE)
        text_surface = self.font20.render("PING:", True, BLACK)
        self.game_screen.blit(text_surface, (20, 20))
        text_surface = self.font20.render(str(self.parent.get_ping()), True, GRAY)
        self.game_screen.blit(text_surface, (20, 40))
        text_surface = self.font20.render("Is connected?:", True, BLACK)
        self.game_screen.blit(text_surface, (20, 100))
        if self.parent.is_connected:
            text_surface = self.font20.render(str("Connected"), True, GREEN)
        else:
            text_surface = self.font20.render(str("Disconnected"), True, RED)
        self.game_screen.blit(text_surface, (20, 120))
        text_surface = self.font36.render(str(threading.active_count()), True, BLACK)
        self.game_screen.blit(text_surface, (300, 60))
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def game_window(self):
        self.game_screen.fill(WHITE)
        pygame.draw.rect(self.game_screen, BLUE, (self.player_x, self.game_height-100, self.player_size, self.player_size))
        pygame.draw.rect(self.game_screen, BLUE, (self.enemy_x, 100, self.player_size, self.player_size))

    def start_button_clicked(self):
        self.is_start_game = False

    def set_enemy_position(self, position_x):
        self.enemy_x = position_x


