import random
import pygame

class Ghost:
    def __init__(self, x, y, speed, color, maze):
        self.x = x
        self.y = y
        self.speed = 2.5
        self.color = color
        self.image = None
        self.maze = maze
        self.direction = random.choice(['right', 'left', 'up', 'down'])

    def move(self):
        if self.direction == 'right' and not self.check_collision(self.x + self.speed, self.y):
            self.x += self.speed
        elif self.direction == 'left' and not self.check_collision(self.x - self.speed, self.y):
            self.x -= self.speed
        elif self.direction == 'up' and not self.check_collision(self.x, self.y - self.speed):
            self.y -= self.speed
        elif self.direction == 'down' and not self.check_collision(self.x, self.y + self.speed):
            self.y += self.speed
        else:
            self.direction = random.choice(['right', 'left', 'up', 'down'])

    def check_collision(self, new_x, new_y):
        maze_width = self.maze.width
        maze_height = self.maze.height
        current_maze = self.maze.mazes[self.maze.nb - 1]
        ghost_rect = pygame.Rect(new_x, new_y, 50, 50)
        for y in range(maze_height):
            for x in range(maze_width):
                if current_maze[x + y * maze_width] == 1:
                    wall_rect = pygame.Rect(x * 50, y * 50, 50, 50)
                    if ghost_rect.colliderect(wall_rect):
                        return True
        return False

    def update(self):
        self.move()

    def draw(self, display):
        if self.image:
            display.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(display, self.color, pygame.Rect(self.x, self.y, 50, 50))