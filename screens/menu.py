import pygame

from constants import WIDTH, HEIGHT
from misc import load_image, terminate
from screens.results import Results


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
        return 255, 255, 0


class MenuLevelButton(MenuButton):
    def __init__(self, rect, text, action, number, is_active=False):
        self.number = number
        self.is_active = is_active
        super().__init__(rect, text, action)

    def get_color(self):
        if self.is_active:
            return 0, 255, 0
        else:
            return 255, 255, 0

    def set_active(self, status):
        self.is_active = status

    def click(self):
        self.action(self.number)


class Menu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width = 800
        self.height = 400
        self.n = 1
        self.text = ['Начать игру', '1 уровень', '2 уровень', '3 уровень', '4 уровень',
                     '5 уровень', 'Закрыть игру', 'Результаты']
        self.rect_positions = [(125, 20, 212, 45), (125, 70, 178, 45), (125, 120, 178, 45),
                               (125, 170, 178, 45), (125, 220, 178, 45), (125, 270, 178, 45),
                               (125, 320, 239, 45), (455, 20, 212, 45)]
        self.buttons = [
            MenuButton(pygame.rect.Rect(self.rect_positions[0]), self.text[0], self.close),
            MenuLevelButton(pygame.rect.Rect(self.rect_positions[1]), self.text[1], self.change_level, 1, True),
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
        while self.running:
            fon = pygame.transform.scale(load_image('menu.jpg'), (WIDTH, HEIGHT))
            self.screen.blit(fon, (0, 0))
            for button in self.buttons:
                button.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.check_mouse_pos(event.pos):
                            button.click()

            pygame.display.flip()
            self.clock.tick(60)

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
        res = Results(self.screen, self.clock)
        res.draw_results()
