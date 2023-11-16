import threading
import time
import pygame
import sys
from WebsocketClientBase import WebsocketClientBase


class GameClient(WebsocketClientBase):
    def __init__(self):
        super().__init__()
        self.server_position = 0
        self.player_x = 0
        t = threading.Thread(target=self.main_pygame)
        t.start()

    def main(self):
        # self.test()
        pass

    def main_pygame(self):
        # Inicjalizacja Pygame
        pygame.init()

        # Ustawienia okna gry
        width, height = 800, 600
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Prosta Gra w Pygame")

        # Ustawienia gracza
        player_size = 50
        self.player_x = 80
        player_y = height - 2 * player_size
        player_speed = 1

        # Ustawienia kolorów
        white = (255, 255, 255)
        blue = (0, 0, 255)

        # Główna pętla gry
        clock = pygame.time.Clock()
        font = pygame.font.Font(pygame.font.get_default_font(), 36)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.player_x > 0:
                self.player_x -= player_speed
                self.test1()

            if keys[pygame.K_RIGHT] and self.player_x < width - player_size:
                self.player_x += player_speed
                self.test1()

            # Wypełnij tło białym kolorem
            screen.fill(white)

            # Narysuj gracza (kwadrat)
            pygame.draw.rect(screen, blue, (self.server_position, player_y, player_size, player_size))
            text_surface = font.render(str(self.get_ping()), True, "red")
            screen.blit(text_surface, (20, 20))
            text_surface = font.render(str(self.is_connected), True, "red")
            screen.blit(text_surface, (300, 20))
            text_surface = font.render(str(threading.active_count()), True, "red")
            screen.blit(text_surface, (300, 60))
            pygame.display.set_caption(f'{clock.get_fps() :.1f}')

            # Zaktualizuj okno
            pygame.display.flip()
            self.test()
            # Ustaw ilość klatek na sekundę
            clock.tick(100)

    def test(self):
        print(self.server_position)
        self.send(method="test", data="", callback=self.call_test)

    def test1(self):
        self.send(method="test1", data=self.player_x, callback=None)

    def call_test(self, callback_mess):
        #print("xd")
        self.player_x = int(callback_mess)
        self.server_position = int(callback_mess)
