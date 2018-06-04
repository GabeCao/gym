class BaseStation:
    def __init__(self):
        self.x = (116.333 - 116.318) * 85000 / 2
        self.y = (40.012 - 39.997) * 110000 / 2

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_time(self):
        return self.time