import os
import random
import sys

import pygame

from sprites.finish import FinishWall
from sprites.obstacle import Obstacle
from sprites.platforms import Platform


def random_colors():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as mess:
        print(f"Файл с изображением '{fullname}' не найден")
        raise SystemExit(mess)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip('\n') for line in mapFile]
        level_map = level_map[::-1]

    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Platform(200 + x * 50, 388 - y * 50, 25, 10)
            elif level[y][x] == '*':
                Obstacle(200 + x * 50, 388 - y * 50, 25, 10)
            elif level[y][x] == '!':
                FinishWall(200 + x * 50, 0, 50, 400)
