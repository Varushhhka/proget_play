import random

import pygame

from constants import GRAVITY, SCREEN_RECT
from misc import load_image
from sprites.groups import particles


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy):
        super().__init__(particles)
        self.fire = [load_image("star_for_firework.png", -1)]
        for scale in (5, 10, 20):
            self.fire.append(pygame.transform.scale(self.fire[0], (scale, scale)))

        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(SCREEN_RECT):
            self.kill()


def create_particles(position):
    particle_count = 50
    numbers = range(-10, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))