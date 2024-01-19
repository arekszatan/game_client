import pygame
from Settings import *
import threading
from Button import Button, buttons_update
from InputBox import InputBox, input_boxes_update
from Bullet import Bullet
import logging as log


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
        self.player_speed = 5
        self.player_size = 50
        self.player_x = 200
        self.enemy_x = 200
        self.next_shoot = True
        self.bullets = []
        self.enemy_bullets = []
        self.my_bullets = []
        self.score = [0, 0]
        self.__item_define()

    def start_game(self):
        self.__main()

    def __main(self):
        for event in pygame.event.get():
            input_boxes_update(event)
            if event.type == pygame.QUIT:
                self.parent.running = False
                pygame.quit()
                return
        if self.parent.is_start_window:
            self.start_window()
            buttons_update()
            input_boxes_update()
        else:
            self.game_window()
            self.check_game_event()
            self.calculate_bullet_position()
        pygame.display.flip()
        self.clock.tick(TIC)

    def __item_define(self):
        Button(self.game_screen, "Start game", 200, 400, 300, 50, self.start_button_clicked)
        self.connect_button = Button(self.game_screen, "Disconnect with room", 200, 460, 300, 50,
                                     self.connect_with_game_room)
        Button(self.game_screen, "Create room", 200, 520, 300, 50, self.create_game_room)
        self.input_name_player = InputBox(self.game_screen, 250, 340, 32, 32, self.set_my_name)

    def check_game_event(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player_x > 0:
            position_tmp = self.player_x - self.player_speed
            self.parent.position_after_move(position_tmp)
        if keys[pygame.K_RIGHT] and self.player_x < self.game_width - self.player_size:
            position_tmp = self.player_x + self.player_speed
            self.parent.position_after_move(position_tmp)
        if keys[pygame.K_SPACE] and self.next_shoot:
            self.shoot()

    def start_window(self):
        self.game_screen.fill(WHITE)
        text_surface = self.font20.render("PING:", True, BLACK)
        self.game_screen.blit(text_surface, (20, 20))
        text_surface = self.font20.render(str(self.parent.get_ping()), True, GRAY)
        self.game_screen.blit(text_surface, (20, 40))
        text_surface = self.font20.render("Is connected with server?:", True, BLACK)
        self.game_screen.blit(text_surface, (20, 100))
        if self.parent.is_connected:
            text_surface = self.font20.render(str("Connected"), True, GREEN)
        else:
            text_surface = self.font20.render(str("Disconnected"), True, RED)
        self.game_screen.blit(text_surface, (20, 120))
        text_surface = self.font20.render("Number of working thread:", True, BLACK)
        self.game_screen.blit(text_surface, (20, 180))
        text_surface = self.font20.render(str(threading.active_count()), True, BLACK)
        self.game_screen.blit(text_surface, (20, 200))
        text_surface = self.font20.render("Is connected with game room?:", True, BLACK)
        self.game_screen.blit(text_surface, (20, 260))
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')
        if self.parent.is_connected_with_room:
            self.connect_button.set_label("Disconnect with room")
            text_surface = self.font20.render(self.parent.my_name_room, True, BLACK)
            self.game_screen.blit(text_surface, (self.game_width - 180, 120))
            text_surface = self.font20.render(self.parent.enemy_name_room, True, BLACK)
            self.game_screen.blit(text_surface, (self.game_width - 180, 140))
            text_surface = self.font20.render(str("Connected"), True, GREEN)
        else:
            self.connect_button.set_label("Connect with room")
            text_surface = self.font20.render("-", True, BLACK)
            self.game_screen.blit(text_surface, (self.game_width - 180, 120))
            text_surface = self.font20.render("-", True, BLACK)
            self.game_screen.blit(text_surface, (self.game_width - 180, 140))
            text_surface = self.font20.render(str("Disconnected"), True, RED)
        self.game_screen.blit(text_surface, (20, 280))
        text_surface = self.font20.render("Your name:", True, BLACK)
        self.game_screen.blit(text_surface, (20, 340))
        text_surface = self.font20.render(self.parent.my_name_room, True, BLACK)
        self.game_screen.blit(text_surface, (20, 360))
        text_surface = self.font20.render(f'Game room {self.parent.room_name}:', True, BLACK)
        self.game_screen.blit(text_surface, (self.game_width - 200, 100))

    def game_window(self):
        self.game_screen.fill(WHITE)
        text_surface = self.font20.render("WYNIK:", True, BLACK)
        self.game_screen.blit(text_surface, (20, 20))
        text_surface = self.font20.render(f'{self.score[0]} / {self.score[1]}', True, GRAY)
        self.game_screen.blit(text_surface, (20, 40))
        pygame.draw.rect(self.game_screen, BLUE, (self.player_x, self.game_height-100, self.player_size,
                                                  self.player_size))
        pygame.draw.rect(self.game_screen, BLUE, (self.enemy_x, 50, self.player_size, self.player_size))

    def shoot(self):
        self.bullets.append(Bullet(self.player_x+self.player_size/2-5, self.game_height-100))
        self.next_shoot = False

    def calculate_bullet_position(self):
        for bullet in self.enemy_bullets:
            if bullet[1] <= 0:
                continue
            pygame.draw.rect(self.game_screen, RED, (int(bullet[0]), self.game_height-20-int(bullet[1]),
                                                     10, 20))
        for bullet in self.my_bullets:
            pygame.draw.rect(self.game_screen, RED, (bullet[0], bullet[1], 10, 20))
        if not self.bullets:
            return
        self.send_bullets_position()
        if self.bullets[-1].get_position_y() < self.game_height - 150:
            self.next_shoot = True
        for bullet in self.bullets:
            bullet.set_position_y(bullet.get_position_y()-self.player_speed)

    def start_button_clicked(self):
        if self.parent.game_is_ready:
            self.parent.is_start_window = False

    def connect_with_game_room(self):
        if not self.parent.is_connected:
            return
        self.parent.connect_with_game_room()

    def create_game_room(self):
        if not self.parent.is_connected:
            return
        self.parent.create_game_room()

    def set_my_name(self, text):
        if self.parent.is_connected_with_room:
            return
        self.parent.my_name_room = text

    def set_enemy_position(self, position_x):
        self.enemy_x = position_x

    def set_enemy_bullets(self, bullets):
        self.enemy_bullets = bullets
        #print(self.enemy_bullets)

    def send_bullets_position(self):
        data = []
        for bullet in self.bullets:
            data.append([bullet.get_position_x(), bullet.get_position_y()])
        self.parent.send(method="send_bullets_position", data=data, callback=self.send_bullets_position_callback)

    def send_bullets_position_callback(self, data):
        self.my_bullets = data
        self.bullets = []
        for bullet in self.my_bullets:
            self.bullets.append(Bullet(bullet[0], bullet[1]))




