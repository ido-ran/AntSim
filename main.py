# Example file showing a circle moving on screen
import pygame
import pygame.freetype
import sys
from dataclasses import dataclass
import random
from math import pi, cos, sin

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

color_map:list = [WHITE, (0, 200, 0), (100,0,0)]

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

WORLD_LOGICAL_WIDTH = 30
WORLD_LOGICAL_HEIGHT = 30

CELL_LOGICAL_SIZE = 4

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

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def angle(self) -> int:
        return self._angle

class Coloney:
    _id: int
    _x: float
    _y: float
    _color: pygame.Color
    _max_ants: int
    _next_ant_id: int = 0
    _ants: list[Ant] = []

    def __init__(self, id: int, x: float, y: float, max_ants: int, color: pygame.Color):
        self._id = id
        self._x = x
        self._y = y
        self._max_ants = max_ants
        self._color = color

        for index in range(5):
            self.create_ant()

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def color(self) -> pygame.Color:
        return self._color

    @property
    def ants(self) -> list[Ant]:
        return self._ants

    def create_ant(self) -> None:
        self._next_ant_id += 1
        ant = Ant(self._next_ant_id, self._x, self._y, random.uniform(0, 2.0 * pi))
        self._ants.append(ant)


world: list[WorldCell] = [WorldCell(0) for index in range(WORLD_LOGICAL_WIDTH * WORLD_LOGICAL_HEIGHT)]
colonies: list[Coloney] = []

def main():
    global WINDOW_HEIGHT, WINDOW_WIDTH

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    screen.fill(BLACK)

    my_font = pygame.freetype.SysFont("Arial", 16)

    # create first coloney
    colonies.append(Coloney(1, 5 * CELL_LOGICAL_SIZE, 5 * CELL_LOGICAL_SIZE, config["max_number_of_ants_in_coloney"], (0,0, 255)))

    while True:
        drawGrid(screen, my_font)
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


def drawGrid(screen, my_font):
    block_width = WINDOW_WIDTH / WORLD_LOGICAL_WIDTH
    block_height = WINDOW_HEIGHT / WORLD_LOGICAL_HEIGHT

    for x in range(0, WORLD_LOGICAL_WIDTH):
        for y in range(0, WORLD_LOGICAL_HEIGHT):
            cell = world[x + y * WORLD_LOGICAL_WIDTH]
            rect = pygame.Rect(x * block_width, y * block_height, block_width, block_height)
            pygame.draw.rect(screen, color_map[cell.color], rect, 1)

            text_surface, rect = my_font.render(f"{x},{y}", (255, 255, 0))
            screen.blit(text_surface, (x * block_width, y * block_height))

    # draw ants
    for coloney in colonies:
        rect = pygame.Rect(coloney.x / CELL_LOGICAL_SIZE * block_width, coloney.y / CELL_LOGICAL_SIZE * block_height, block_width, block_height)
        pygame.draw.rect(screen, coloney.color, rect, 2)

        for ant in coloney.ants:
            ant_size = block_width / CELL_LOGICAL_SIZE
            ant_center_x = ant.x / CELL_LOGICAL_SIZE * block_width
            ant_center_y = ant.y / CELL_LOGICAL_SIZE * block_height
            pygame.draw.circle(screen, coloney.color, (ant_center_x, ant_center_y), ant_size)

            dir = pygame.Vector2(cos(ant.angle), sin(ant.angle))
            pygame.draw.line(screen, (255,255,255),
                             (ant_center_x + dir.x, ant_center_y),
                             (ant_center_x + dir.x * ant_size, ant_center_y + dir.y * ant_size),
                             3)

if __name__ == "__main__":
    main()
