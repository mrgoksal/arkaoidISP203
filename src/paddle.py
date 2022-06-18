from configs import *

# Инициализация отбивочной доски
class Paddle:
    def __init__(self):
        self.width = PADDLE_W
        self.height = PADDLE_H
        self.speed = PADDLE_SPEED
        self.rect = pygame.Rect(WIDTH // 2 - self.width // 2, HEIGHT - self.height - 10, self.width, self.height)
