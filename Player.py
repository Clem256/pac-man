class Player :
    x = 50
    y = 50
    speed = 2.5

    def right(self):
        self.x = self.x + self.speed
    def left(self):
        self.x = self.x - self.speed
    def up(self):
        self.y = self.y - self.speed
    def down(self):
        self.y = self.y + self.speed