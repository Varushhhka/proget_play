import pygame

from constants import WIDTH, HEIGHT
from misc import load_image, terminate


class Results:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width = 800
        self.height = 400

    def draw_results(self):
        fon = pygame.transform.scale(load_image('menu.jpg'), (WIDTH, HEIGHT))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 60

        text = 'УРОВЕНЬ - РЕЗУЛЬТАТ'
        string_rendered = font.render(text, True, pygame.Color('green'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 30
        intro_rect.x = 250

        self.screen.blit(string_rendered, intro_rect)
        pygame.draw.rect(self.screen, (0, 255, 0), (240, 20, 260, 40), 3)

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
                intro_rect.x = 250
                text_coord += intro_rect.height
                self.screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return

            pygame.display.flip()
            self.clock.tick(60)
