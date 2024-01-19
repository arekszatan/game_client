class Bullet:
    def __init__(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y

    def get_position_x(self):
        return self.position_x

    def get_position_y(self):
        return self.position_y

    def set_position_y(self, position):
        self.position_y = position
