import os
import sys

import pygame

pygame.init()


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
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Character(pygame.sprite.Sprite):
    gravity = 0.4
    jump_height = 8

    def __init__(self, x, y, size):
        super().__init__(all_sprites, character_group)
        self.size = size
        self.image = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color("green"), (0, 0, size, size))
        self.rect = pygame.Rect(x, y, size, size)
        self.velocity = 0

    def update(self):
        self.move()
        self.check_kill()

    def check_kill(self):
        if pygame.sprite.spritecollideany(self, obstacle_group):
            self.kill()
            pygame.quit()

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


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(all_sprites, movable_group, obstacle_group)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color("red"), (0, 0, w, h))
        self.rect = pygame.Rect(x, y, w, h)


class Camera:
    def __init__(self):
        self.dx = -2

    def apply(self):
        for obj in movable_group:
            obj.rect.x += self.dx


def start_screen():
    intro_text = ["ЗАСТАВКА"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(60)


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Platform(200 + x * 50, 388 - y * 50, 25, 10)
            elif level[y][x] == '*':
                Obstacle(200 + x * 25,    388 - y * 10, 25, 10)


all_sprites = pygame.sprite.Group()
character_group = pygame.sprite.Group()
movable_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
platforms = pygame.sprite.Group()

SCREEN_SIZE = WIDTH, HEIGHT = 800, 400
CHARACTER_SIZE = 20
screen = pygame.display.set_mode(SCREEN_SIZE)
camera = Camera()

level = load_level('1level.txt')
generate_level(level)

base = MainPlatform()
character = Character(WIDTH // 8 - CHARACTER_SIZE // 2, HEIGHT - CHARACTER_SIZE - 2, CHARACTER_SIZE)

clock = pygame.time.Clock()
running = True
start_screen()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                character.jump()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    camera.apply()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
