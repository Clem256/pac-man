import pygame
import time
from pygame.locals import *
from Maze import Maze
from Player import Player
from Ghost import Ghost
from tkinter import Tk, messagebox
import random


class pac_man:
    windowWidth = 800
    windowHeight = 600
    player = 0

    def __init__(self):
        self._running = True
        self._display = None
        self._image = None
        self._block = None
        self.player = Player()
        self.maze = Maze()
        self.nb = 1
        self.score = 0
        self.score_increment = 10
        self.ghosts = [
            Ghost(250, 250, 1.5, (255, 0, 0), self.maze),
            Ghost(400, 400, 1.5, (255, 192, 203), self.maze),
            Ghost(300, 300, 1.5, (0, 0, 255), self.maze)
        ]
        self.is_moving = False
        self.current_direction = None
        self.windowWidth = self.maze.width * 50
        self.windowHeight = self.maze.height * 50
        self.konami_code = [K_z, K_z, K_s, K_s, K_q, K_d, K_q, K_d, K_b, K_a]
        self.konami_index = 0
        self.last_input_time = time.time()
        self.input_delay = 0.1
        self.RedGhost_Small = None
        self.YellowGhost_Small = None
        self.PurpleGhostSmall = None
        self.BlueGhostSmall = None

    def on_init(self):
        pygame.init()
        self._display = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.RESIZABLE)
        pygame.display.set_caption("Pac man")
        self._running = True
        pygame.joystick.init()
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Joystick détecté : {self.joystick.get_name()}")
        else:
            print("Aucun joystick détecté.")
        PlayerImage = pygame.image.load("pacman/pacman.png").convert()
        BlockImage = pygame.image.load("pacman/texture.png").convert()
        RedGhostImage = pygame.image.load("pacman/red_ghost.png").convert_alpha()
        YellowGhostImage = pygame.image.load("pacman/yellow_gost.webp").convert_alpha()
        PurpleGhostImage = pygame.image.load("pacman/purple.png").convert_alpha()
        BlueGhostImage = pygame.image.load("pacman/blue.png").convert_alpha()
        PointImage = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(PointImage, (255, 255, 255), (12, 12), 5)
        Player_Small = pygame.transform.scale(PlayerImage, (40, 40))
        Block_Small = pygame.transform.scale(BlockImage, (50, 50))
        Point_Small = pygame.transform.scale(PointImage, (50, 50))
        RedGhost_Small = pygame.transform.scale(RedGhostImage, (40, 40))
        YellowGhost_Small = pygame.transform.scale(YellowGhostImage, (40, 40))
        PurpleGhostSmall = pygame.transform.scale(PurpleGhostImage, (40, 40))
        BlueGhostSmall = pygame.transform.scale(BlueGhostImage, (40, 40))
        self._image = Player_Small
        self._block = Block_Small
        self._point = Point_Small
        self.RedGhost_Small = RedGhost_Small
        self.YellowGhost_Small = YellowGhost_Small
        self.PurpleGhostSmall = PurpleGhostSmall
        self.BlueGhostSmall = BlueGhostSmall
        self.ghosts[0].image = RedGhost_Small
        self.ghosts[1].image = YellowGhost_Small
        self.ghosts[2].image = PurpleGhostSmall

    def on_event(self, event):
        current_time = time.time()

        # Gestion des événements clavier
        if event.type == KEYDOWN:
            # Vérification du Konami Code
            if current_time - self.last_input_time >= self.input_delay:
                if event.key == self.konami_code[self.konami_index]:
                    self.konami_index += 1
                    self.last_input_time = current_time
                    if self.konami_index == len(self.konami_code):
                        self.change_maze()
                        self.konami_index = 0

                else:
                    self.konami_index = 0
                    self.last_input_time = current_time

            # Contrôles classiques au clavier
            if event.key == K_RIGHT:
                self.current_direction = 'right'
                self.is_moving = True
            elif event.key == K_LEFT:
                self.current_direction = 'left'
                self.is_moving = True
            elif event.key == K_UP:
                self.current_direction = 'up'
                self.is_moving = True
            elif event.key == K_DOWN:
                self.current_direction = 'down'
                self.is_moving = True

        elif event.type == KEYUP:
            # Arrêt du mouvement clavier
            if event.key in [K_RIGHT, K_LEFT, K_UP, K_DOWN]:
                self.is_moving = False

        elif event.type == pygame.JOYAXISMOTION and self.joystick:
            axis_x = self.joystick.get_axis(0)
            axis_y = self.joystick.get_axis(1)

            if axis_x > 0.5:
                self.current_direction = 'right'
                self.is_moving = True
            elif axis_x < -0.5:
                self.current_direction = 'left'
                self.is_moving = True
            elif axis_y > 0.5:
                self.current_direction = 'down'
                self.is_moving = True
            elif axis_y < -0.5:
                self.current_direction = 'up'
                self.is_moving = True
            else:
                self.is_moving = False


    def loop(self):
        if self.is_moving:
            if self.current_direction == 'right':
                self.player.right()
            elif self.current_direction == 'left':
                self.player.left()
            elif self.current_direction == 'up':
                self.player.up()
            elif self.current_direction == 'down':
                self.player.down()

    def check_collision_with_ghosts(self):
        player_rect = pygame.Rect(self.player.x, self.player.y, 40, 40)
        for ghost in self.ghosts:
            ghost_rect = pygame.Rect(ghost.x, ghost.y, 50, 50)
            if player_rect.colliderect(ghost_rect):
                tk = Tk()
                tk.withdraw()
                if ghost.color == (255, 0, 0):
                    messagebox.showinfo("Game Over", "Gustave, the red ghost, killed you!")
                elif ghost.color == (255, 192, 203):
                    messagebox.showinfo("Game Over", "Gustavo, the yellow ghost, killed you!")
                elif ghost.color == (0, 0, 255):
                    messagebox.showinfo("Game Over", "Nils , the blue ghost, killed you!")
                self._running = False
                tk.destroy()
                break

    def render(self):
        self._display.fill((0, 0, 0))
        self.maze.draw(self._display, self._block, self._point)
        player_rect = pygame.Rect(self.player.x, self.player.y, 40, 40)
        current_maze = self.maze.mazes[self.maze.nb - 1]

        keys = pygame.key.get_pressed()
        moving_right = keys[K_RIGHT]
        moving_left = keys[K_LEFT]
        moving_up = keys[K_UP]
        moving_down = keys[K_DOWN]

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                index = x + y * self.maze.width
                if index >= len(current_maze):
                    continue  # Éviter l'erreur pour diagnostiquer

                tile = current_maze[index]
                if tile == 1:
                    wall_rect = pygame.Rect(x * 50, y * 50, 50, 50)
                    if player_rect.colliderect(wall_rect):
                        if moving_right:
                            self.player.x = wall_rect.left - player_rect.width
                        elif moving_left:
                            self.player.x = wall_rect.right
                        elif moving_down:
                            self.player.y = wall_rect.top - player_rect.height
                        elif moving_up:
                            self.player.y = wall_rect.bottom
                elif tile == '.':
                    point_rect = pygame.Rect(x * 50, y * 50, 50, 50)
                    if player_rect.colliderect(point_rect):
                        current_maze[index] = 0
                        self.maze.points.remove((x, y))
                        self.score += self.score_increment
                    else:
                        self._display.blit(self._point, (x * 50, y * 50))

        self._display.blit(self._image, (self.player.x, self.player.y))
        #pygame.draw.rect(self._display, (255, 0, 0), player_rect, 2)
        for ghost in self.ghosts:
            ghost.update()
            ghost.draw(self._display)
            ghost_rect = pygame.Rect(ghost.x, ghost.y, 50, 50)
            #pygame.draw.rect(self._display, (0, 255, 0), ghost_rect, 2)

        font = pygame.font.SysFont('Arial', 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self._display.blit(score_text, (10, 10))
        pygame.display.flip()

    def end(self):
        pygame.quit()

    def change_maze(self):
        self.maze.nb = (self.maze.nb % len(self.maze.mazes)) + 1
        self.maze.points = set()
        current_maze = self.maze.mazes[self.maze.nb - 1]
        for i, tile in enumerate(current_maze):
            if tile == '.':
                self.maze.points.add((i % self.maze.width, i // self.maze.width))
        self.player.x = 50
        self.player.y = 50
        self.ghosts.clear()

        # Initialisation des fantômes avec des positions fixes selon le labyrinthe
        if self.maze.nb == 3:
            self.ghosts = [
                Ghost(250, 250, 1.5, (255, 0, 0), self.maze),
                Ghost(500, 400, 1.5, (255, 192, 203), self.maze),
                Ghost(800, 400, 1.5, (0, 0, 255), self.maze),
                Ghost(1400, 600, 1.5, (0, 255, 0), self.maze)
            ]
            self.ghosts[0].image = self.RedGhost_Small
            self.ghosts[1].image = self.YellowGhost_Small
            self.ghosts[2].image = self.PurpleGhostSmall
            self.ghosts[3].image = self.BlueGhostSmall
        elif self.maze.nb == 2:
            self.ghosts = [
                Ghost(1000, 400, 1.5, (255, 0, 0), self.maze),
                Ghost(250, 250, 1.5, (255, 192, 203), self.maze),
                Ghost(300, 300, 1.5, (0, 0, 255), self.maze)
            ]
            self.ghosts[0].image = self.RedGhost_Small
            self.ghosts[1].image = self.YellowGhost_Small
            self.ghosts[2].image = self.PurpleGhostSmall
        else:
            self.ghosts = [
                Ghost(150, 150, 1.5, (255, 0, 0), self.maze),
                Ghost(250, 250, 1.5, (255, 192, 203), self.maze),
                Ghost(350, 350, 1.5, (0, 0, 255), self.maze)
            ]
            self.ghosts[0].image = self.RedGhost_Small
            self.ghosts[1].image = self.YellowGhost_Small
            self.ghosts[2].image = self.BlueGhostSmall

    def run(self):
        if self.on_init() == False:
            self._running = False
        while self._running:
            clock = pygame.time.Clock()
            clock.tick(60)
            events = pygame.event.get()
            for event in events:
                self.on_event(event)
            keys = pygame.key.get_pressed()
            if keys[K_RIGHT]:
                self.player.right()
            if keys[K_LEFT]:
                self.player.left()
            if keys[K_UP]:
                self.player.up()
            if keys[K_DOWN]:
                self.player.down()
            if keys[K_ESCAPE]:
                tk = Tk()
                tk.withdraw()
                answer = messagebox.askquestion("Do you really leave", "Do you need to quit this magnificent game?")
                tk.destroy()
                if answer == 'yes':
                    self._running = False
                elif answer == 'no':
                    pass

            self.check_collision_with_ghosts()
            self.loop()
            self.render()
            if self.maze.count_points() == 0:
                print("win")
                tk = Tk()
                tk.withdraw()
                messagebox.showinfo("GG", "You win the stage")
                tk.destroy()
                self.change_maze()
        self.end()






if __name__ == "__main__":
    game = pac_man()
    game.run()
