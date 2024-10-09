from time import sleep

import pygame
from Pawn import Pawn, Position
from config import Config

pygame.init()


class Game:
    def __init__(self):
        display = pygame.display.set_mode(Config.SCREEN_SIZE)
        self.display = display
        self.clock = pygame.time.Clock()
        self.maze = []
        # WallID -> "ver_wall#{row}-{col}" or "hor_wall#{row}-{col}"
        self.walls = []
        self.possible_walls = []
        self.green_pawn = Pawn('Green', Position(*Config.GREEN_PAWN_START_POSITION), self.walls)
        self.red_pawn = Pawn('Red', Position(*Config.RED_PAWN_START_POSITION), self.walls)
        self.reset()
        self._updateUI()

    def _updateUI(self):
        self.display.fill(Config.BACKGROUND_COLOR)
        # --Frame
        # -Top Up
        pygame.draw.rect(self.display, Config.FRAME_COLOR, (0, 0, 550, 10))
        # -Top Down
        pygame.draw.rect(self.display, Config.FRAME_COLOR, (0, 50, 550, 10))
        # -Left
        pygame.draw.rect(self.display, Config.FRAME_COLOR, (0, 0, 10, 600))
        # -Right
        pygame.draw.rect(self.display, Config.FRAME_COLOR, (540, 0, 10, 600))
        # -Bottom
        pygame.draw.rect(self.display, Config.FRAME_COLOR, (0, 590, 550, 10))

        # Lines
        x, y = 10, 60
        for row in range(Config.MAP_SIZE):
            for col in range(Config.MAP_SIZE):
                if row != Config.MAP_SIZE - 1:
                    pygame.draw.rect(self.display, Config.LINE_COLOR, (x + 50, y, 10, 50))
                if col != Config.MAP_SIZE - 1:
                    pygame.draw.rect(self.display, Config.LINE_COLOR, (x, y + 50, 50, 10))
                x += 60
            x = 10
            y += 60
        # Walls
        self.walls.append('hor_wall#0-0')
        for wall in self.walls:
            x, y = tuple(map(int, wall.split('#')[1].split('-')))
            x = x * 60 + 10
            y = y * 60
            if wall.startswith('ver_wall'):
                pygame.draw.rect(self.display, Config.LINE_COLOR, (x + 50, y, 10, 50))
            else:
                pygame.draw.rect(self.display, Config.LINE_COLOR, (x, y + 50, 50, 10))

        # Pawns
        pawn_x, pawn_y = self.green_pawn.position.col * 60 + 35, self.green_pawn.position.row * 60 + 85
        pygame.draw.circle(self.display, self.green_pawn.color, (pawn_x, pawn_y), 15)
        pawn_x, pawn_y = self.red_pawn.position.col * 60 + 35, self.red_pawn.position.row * 60 + 85
        pygame.draw.circle(self.display, self.red_pawn.color, (pawn_x, pawn_y), 15)
        pygame.display.flip()

    def reset(self):
        pass


game = Game()
sleep(100)