import pygame

from constants import HEIGHT, WIDTH
from sprites.groups import all_sprites, platforms, movable_group


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, is_movable=True, color=pygame.Color("yellow")):
        super().__init__(all_sprites, platforms)
        if is_movable:
            self.add(movable_group)

        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, color, (0, 0, w, h))
        self.rect = pygame.Rect(x, y, w, h)


class MainPlatform(Platform):
    def __init__(self):
        super().__init__(0, HEIGHT - 2, WIDTH, 20, False, pygame.Color("white"))
