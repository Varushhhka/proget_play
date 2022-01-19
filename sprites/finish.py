import pygame

from sprites.groups import all_sprites, movable_group, finish_group


class FinishWall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(all_sprites, movable_group, finish_group)

        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color("blue"), (0, 0, w, h))
        self.rect = pygame.Rect(x, y, w, h)
