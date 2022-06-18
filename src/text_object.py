import pygame
import pygame.freetype


class TextObject:
    # Инициализация текстового поля
    def __init__(self, x, y, message, color=(110, 110, 110), font_size=50):
        self.pos = (x, y)
        self.message = message
        self.color = color
        pygame.font.init()
        self.font = pygame.font.SysFont('1', font_size)  # Описание шрифта
        self.bounds = self.get_surface(message)

    # Метод отрисовки
    def draw(self, surface, centralized=False):
        text_surface, self.bounds = \
            self.get_surface(self.message)
        if centralized:
            pos = (self.pos[0] - self.bounds.width // 2,
                   self.pos[1])
        else:
            pos = self.pos
        surface.blit(text_surface, pos)

    # Метод рендера шрифта (нужно для отрисовки 
    def get_surface(self, text):
        text_surface = self.font.render(text, False, self.color)
        return text_surface, text_surface.get_rect()
