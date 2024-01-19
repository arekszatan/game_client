from Settings import *
import logging as log
all_buttons = []


def buttons_update():
    for button in all_buttons:
        button.draw_button()
        button.check_clicked()


class Button:
    def __init__(self, screen, text, position_x, position_y, width, height, callback=None):
        self.screen = screen
        self.text = text
        self.callback = callback
        self.button_width = width
        self.button_height = height
        self.button_position_x = position_x
        self.button_position_y = position_y
        self.color = GRAY
        self.font_color = WHITE
        self.font_size = 25
        self.button_rect = pg.Rect(self.button_position_x, self.button_position_y, self.button_width, self.button_height)
        self.is_clicked = False
        all_buttons.append(self)

    def check_clicked(self):
        mouse = pg.mouse.get_pressed()
        if mouse[0]:
            if not self.button_rect.collidepoint(pg.mouse.get_pos()):
                return
            if self.is_clicked:
                return
            self.is_clicked = True
            if self.callback is not None:
                self.callback()
                log.info(f'Button is clicked and method {self.callback.__name__} is proceeding')
        else:
            self.is_clicked = False

    def draw_button(self):
        if self.is_clicked:
            self.color = (34, 195, 210)
            self.font_color = BLACK
        else:
            self.color = GRAY
            self.font_color = WHITE
        pg.draw.rect(self.screen, self.color, self.button_rect)
        font = pg.font.Font(None, self.font_size)
        text_surface = font.render(self.text, True, self.font_color)
        text_rect = text_surface.get_rect(center=self.button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def set_label(self, text):
        self.text = text
