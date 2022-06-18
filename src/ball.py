from configs import *

# Класс мяча и его характеристики
class Ball:
    def __init__(self):
        self.radius = BALL_RADIUS
        self.speed = BALL_SPEED
        # Расчет коллизии мяча на основе ширины и высоты экрана (круг)
        self.g_rect = int(self.radius * 2 ** 0.5)
        self.rect = pygame.Rect(rnd(self.g_rect, WIDTH - self.g_rect), HEIGHT // 2, self.g_rect, self.g_rect)
        self.dx = 1
        self.dy = -1
