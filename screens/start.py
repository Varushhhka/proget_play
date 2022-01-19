import pygame

from constants import WIDTH, HEIGHT
from misc import load_image, terminate


def start_screen(screen, clock, text, image, n=0):
    intro_text = text
    fon = pygame.transform.scale(load_image(image, n), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 20

    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('green'))
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