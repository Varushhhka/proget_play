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
            global alive
            self.kill()
            alive = False

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


def start_screen(text, image):
    intro_text = [text]
    fon = pygame.transform.scale(load_image(image), (WIDTH, HEIGHT))
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


class MenuButton:
    def __init__(self, rect, text, action):
        self.rect = rect
        self.text = text
        self.action = action

    def draw(self, screen):
        font = pygame.font.Font(None, 50)
        text = font.render(self.text, True, self.get_color())
        surface = pygame.surface.Surface(self.rect.size, pygame.SRCALPHA)
        surface.blit(text, (4, 4))
        pygame.draw.rect(surface, (0, 255, 0), pygame.rect.Rect((0, 0), self.rect.size), 3)
        screen.blit(surface, self.rect)

    def check_mouse_pos(self, pos):
        return self.rect.collidepoint(*pos)

    def click(self):
        self.action()

    def get_color(self):
        return (255, 255, 0)


class MenuLevelButton(MenuButton):
    def __init__(self, rect, text, action, number, is_active=False):
        self.number = number
        self.is_active = is_active
        super().__init__(rect, text, action)

    def get_color(self):
        if self.is_active:
            return (0, 255, 0)
        else:
            return (255, 255, 0)

    def set_active(self, status):
        self.is_active = status

    def click(self):
        self.action(self.number)


class Menu:
    def __init__(self):
        self.width = 800
        self.height = 400
        self.n = 1
        self.text = ['Начать игру', '1 уровень', '2 уровень', '3 уровень', '4 уровень',
                     '5 уровень', 'Закрыть игру', 'Результаты']
        self.rect_positions = [(25, 20, 212, 45), (25, 70, 178, 45), (25, 120, 178, 45),
                               (25, 170, 178, 45), (25, 220, 178, 45), (25, 270, 178, 45),
                               (25, 320, 239, 45), (555, 20, 212, 45)]
        self.buttons = [
            MenuButton(pygame.rect.Rect(self.rect_positions[0]), self.text[0], self.close),
            MenuLevelButton(pygame.rect.Rect(self.rect_positions[1]), self.text[1], self.change_level, 1),
            MenuLevelButton(pygame.rect.Rect(self.rect_positions[2]), self.text[2], self.change_level, 2),
            MenuLevelButton(pygame.rect.Rect(self.rect_positions[3]), self.text[3], self.change_level, 3),
            MenuLevelButton(pygame.rect.Rect(self.rect_positions[4]), self.text[4], self.change_level, 4),
            MenuLevelButton(pygame.rect.Rect(self.rect_positions[5]), self.text[5], self.change_level, 5),
            MenuButton(pygame.rect.Rect(self.rect_positions[6]), self.text[6], terminate),
            MenuButton(pygame.rect.Rect(self.rect_positions[7]), self.text[7], self.results)
        ]
        self.running = True

    def return_level(self):
        return self.n

    def draw_menu(self):
        fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

        while self.running:
            for button in self.buttons:
                button.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.check_mouse_pos(event.pos):
                            button.click()
            pygame.display.flip()
            clock.tick(60)

    def close(self):
        self.running = False

    def change_level(self, n):
        for button in self.buttons:
            if isinstance(button, MenuLevelButton):
                if button.number != n:
                    button.set_active(False)
                else:
                    button.set_active(True)
        self.n = n

    def results(self):
        res = Results()
        res.draw_results()


class Results():
    def __init__(self):
        self.width = 800
        self.height = 400

    def draw_results(self):
        fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 40
        string_rendered = font.render('УРОВЕНЬ - РЕЗУЛЬТАТ', True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 10
        intro_rect.x = 10
        screen.blit(string_rendered, intro_rect)

        with open('results.txt') as f:
            lines = f.readlines()
            lines = lines[:10]
            for line in lines:
                line = line.split()
                if line[1] == '1':
                    message = 'ПРОЙДЕНО'
                    string_rendered = font.render(f'{line[0]} уровень - {message}', True, pygame.Color('green'))
                else:
                    message = 'ПРОВАЛЕНО'
                    string_rendered = font.render(f'{line[0]} уровень - {message}', True, pygame.Color('red'))
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
                Obstacle(200 + x * 25, 388 - y * 10, 25, 10)


all_sprites = pygame.sprite.Group()
character_group = pygame.sprite.Group()
movable_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
platforms = pygame.sprite.Group()

SCREEN_SIZE = WIDTH, HEIGHT = 800, 400
CHARACTER_SIZE = 20
screen = pygame.display.set_mode(SCREEN_SIZE)
camera = Camera()

clock = pygame.time.Clock()

start_screen('Нажмите для начала игры', 'fon.jpg')
while True:
    base = MainPlatform()
    character = Character(WIDTH // 8 - CHARACTER_SIZE // 2, HEIGHT - CHARACTER_SIZE - 2, CHARACTER_SIZE)

    menu = Menu()
    menu.draw_menu()
    n = menu.return_level()
    level = load_level(str(n) + 'level.txt')
    generate_level(level)

    alive = True
    finish = False
    running = True
    while running:
        if not alive:
            running = False
        elif finish:
            running = False
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
    if finish:
        start_screen('Вы выиграли!', 'fon.jpg')
        with open('results.txt') as file:
            lines = file.readlines()
            lines.insert(0, f'{str(n)} 1\n')
        with open('results.txt', 'w') as file:
            for line in lines:
                file.write(line)
    else:
        start_screen('Вы проиграли!', 'fon.jpg')
        with open('results.txt') as file:
            lines = file.readlines()
            lines.insert(0, f'{str(n)} 0\n')
        with open('results.txt', 'w') as file:
            for line in lines:
                file.write(line)
    for sprite in all_sprites:
        sprite.kill()
pygame.quit()