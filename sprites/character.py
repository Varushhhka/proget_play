import pygame

from misc import random_colors
from sprites.groups import platforms, finish_group, obstacle_group, character_group, all_sprites


class Character(pygame.sprite.Sprite):
    gravity = 0.4
    jump_height = 8

    def __init__(self, x, y, size):
        super().__init__(all_sprites, character_group)
        self.velocity = 0
        self.ticks = 0
        self.size = size
        self.cur_color = 0
        self.colors = [random_colors() for _ in range(20)]

        self.image = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, self.colors[self.cur_color], (0, 0, size, size))
        self.rect = pygame.Rect(x, y, size, size)

        self.finish = False
        self.alive = True

    def update(self):
        self.ticks += 1
        if self.ticks % 10 == 0:
            self.cur_color = (self.cur_color + 1) % len(self.colors)
            pygame.draw.rect(self.image, self.colors[self.cur_color], (0, 0, self.size, self.size))

        self.move()
        self.check_kill()
        self.check_finish()

    def check_kill(self):
        if pygame.sprite.spritecollideany(self, obstacle_group):
            self.kill()
            self.alive = False

    def check_finish(self):
        if pygame.sprite.spritecollideany(self, finish_group):
            self.kill()
            self.finish = True

    def move(self):
        collision = pygame.sprite.spritecollideany(self, platforms)
        if collision:
            if self.velocity != 0:
                self.rect.y = collision.rect.y - self.size + 1
            self.velocity = 0
        else:
            self.velocity += self.gravity
        self.rect = self.rect.move(0, self.velocity)

    def jump(self):
        if self.can_jump():
            self.velocity = -self.jump_height
            self.rect = self.rect.move(0, -1)

    def can_jump(self):
        return bool(pygame.sprite.spritecollideany(self, platforms))

    def is_finished(self):
        return self.finish

    def is_alive(self):
        return self.alive
