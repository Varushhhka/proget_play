import pygame

from constants import SCREEN_SIZE, WIDTH, CHARACTER_SIZE, HEIGHT
from misc import load_level, generate_level
from screens.menu import Menu
from screens.start import start_screen
from sprites.camera import Camera
from sprites.character import Character
from sprites.groups import all_sprites
from sprites.platforms import MainPlatform

pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
camera = Camera()
clock = pygame.time.Clock()

start_screen(screen, clock, [], 'start_screen.jpg')
while True:
    base = MainPlatform()
    character = Character(WIDTH // 8 - CHARACTER_SIZE // 2, HEIGHT - CHARACTER_SIZE - 2, CHARACTER_SIZE)

    menu = Menu(screen, clock)
    menu.draw_menu()
    n = menu.return_level()
    level = load_level(str(n) + 'level.txt')
    generate_level(level)

    running = True
    while running:
        if not character.is_alive() or character.is_finished():
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

    if character.is_finished():
        start_screen(screen, clock, ['Вы выиграли,', 'какая жАлОсть!'], 'win.jpg')
        with open('results.txt') as file:
            lines = file.readlines()
            lines.insert(0, f'{str(n)} 1\n')
        with open('results.txt', 'w') as file:
            for line in lines:
                file.write(line)
    else:
        start_screen(screen, clock, ['Вы проиграли,', 'какая прЕлЕсть!'], 'gameover.jpg')
        with open('results.txt') as file:
            lines = file.readlines()
            lines.insert(0, f'{str(n)} 0\n')
        with open('results.txt', 'w') as file:
            for line in lines:
                file.write(line)

    for sprite in all_sprites:
        sprite.kill()
