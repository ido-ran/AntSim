# Example file showing a circle moving on screen
import pygame
import sys
from dataclasses import dataclass
import random
from math import pi

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

color_map:list = [(0, 200, 0), WHITE, (100,0,0)]

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

WORLD_WIDTH = 30
WORLD_HEIGHT = 30

config = {
    "max_number_of_ants_in_coloney": 100
}

@dataclass
class WorldCell:
    color: int

class Ant:
    def __init__(self, id: int, x: float, y: float, angle: float):
        self._id = id
        self._x = x
        self._y = y
        self._angle = angle

class Coloney:
    _id: int
    _x: float
    _y: float
    _max_ants: int
    _next_ant_id: int = 0
    _ants: list[Ant] = []

    def __init__(self, id: int, x: float, y: float, max_ants: int):
        self._id = id
        self._x = x
        self._y = y
        self._max_ants = max_ants

        for index in range(5):
            self.create_ant()

    def create_ant(self) -> None:
        self._next_ant_id += 1
        ant = Ant(self._next_ant_id, self._x, self._y, random.uniform(0, 2.0 * pi))
        self._ants.append(ant)

world: list[WorldCell] = [WorldCell((index // 30) % 3) for index in range(WORLD_WIDTH * WORLD_HEIGHT)]
colonies: list[Coloney] = []

def main():
    global WINDOW_HEIGHT, WINDOW_WIDTH

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    screen.fill(BLACK)

    # create first coloney
    colonies.append(Coloney(1, config["max_number_of_ants_in_coloney"]))

    while True:
        drawGrid(screen)
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                WINDOW_HEIGHT = event.h
                WINDOW_WIDTH = event.w

        pygame.display.update()
        clock.tick(60)


def drawGrid(screen):
    block_width = WINDOW_WIDTH / WORLD_WIDTH
    block_height = WINDOW_HEIGHT / WORLD_HEIGHT

    for x in range(0, WORLD_WIDTH):
        for y in range(0, WORLD_HEIGHT):
            cell = world[x + y * WORLD_WIDTH]
            rect = pygame.Rect(x * block_width, y * block_height, block_width, block_height)
            pygame.draw.rect(screen, color_map[cell.color], rect, 1)


if __name__ == "__main__":
    main()
