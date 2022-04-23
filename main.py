import pygame

from configs import *
from src.ball import Ball
from src.paddle import Paddle
from src.button import Button
from src.blocks import Blocks


class Game:
    def __init__(self):
        self.img = None
        self.clock = None
        self.sc = None
        self.fps = FPS
        self.width = WIDTH
        self.height = HEIGHT

        # Menu
        self.is_menu = True

        # Ball
        self.ball = Ball()

        # Paddle
        self.paddle = Paddle()

        # Blocks
        self.blocks = Blocks()

    def run(self):
        pygame.init()
        self.sc = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # background image
        self.img = pygame.image.load('images/background.jpg').convert()
        self.img = pygame.transform.scale(self.img, (WIDTH, HEIGHT))

        # game running
        while True:
            if not self.show_menu():
                return
            self.game_loop()

    def restart(self):
        self.is_menu = True
        self.ball = Ball()
        self.paddle = Paddle()
        self.blocks = Blocks()

    def detect_collision(self):
        if self.ball.dx > 0:
            delta_x = self.ball.rect.right - self.paddle.rect.left
        else:
            delta_x = self.paddle.rect.right - self.ball.rect.left
        if self.ball.dy > 0:
            delta_y = self.ball.rect.bottom - self.paddle.rect.top
        else:
            delta_y = self.paddle.rect.bottom - self.ball.rect.top

        if abs(delta_x - delta_y) < 10:
            self.ball.dx, self.ball.dy = -self.ball.dx, -self.ball.dy
        elif delta_x > delta_y:
            self.ball.dy = -self.ball.dy
        elif delta_y > delta_x:
            self.ball.dx = -self.ball.dx
        return self.ball.dx, self.ball.dy

    def game_loop(self):
        while not self.is_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            self.sc.blit(self.img, (0, 0))

            # drawing world
            [pygame.draw.rect(self.sc, self.blocks.color_list[color], block) for color, block in
             enumerate(self.blocks.block_list)]

            pygame.draw.rect(self.sc, pygame.Color('darkorange'), self.paddle)

            pygame.draw.circle(self.sc, pygame.Color('white'), self.ball.rect.center, self.ball.radius)

            # ball movement
            self.ball.rect.x += self.ball.speed * self.ball.dx
            self.ball.rect.y += self.ball.speed * self.ball.dy

            # collision left right
            if self.ball.rect.centerx < self.ball.radius or self.ball.rect.centerx > WIDTH - self.ball.radius:
                self.ball.dx = -self.ball.dx

            # collision top
            if self.ball.rect.centery < self.ball.radius:
                self.ball.dy = -self.ball.dy

            # collision paddle
            if self.ball.rect.colliderect(self.paddle) and self.ball.dy > 0:
                self.ball.dx, self.ball.dy = self.detect_collision()

            # collision blocks
            hit_index = self.ball.rect.collidelist(self.blocks.block_list)
            if hit_index != -1:
                hit_rect = self.blocks.block_list.pop(hit_index)
                hit_color = self.blocks.color_list.pop(hit_index)
                self.ball.dx, self.ball.dy = self.detect_collision()

                # special effect
                hit_rect.inflate_ip(self.ball.rect.width * 3, self.ball.rect.height * 3)
                pygame.draw.rect(self.sc, hit_color, hit_rect)
                self.fps += 2

            # win, game over
            if self.ball.rect.bottom > HEIGHT:
                print('GAME OVER!')
                self.restart()
                return False
            elif not len(self.blocks.block_list):
                print('WIN!!!')
                self.restart()
                return True

            # control
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.paddle.rect.left > 0:
                self.paddle.rect.left -= self.paddle.speed
            if key[pygame.K_RIGHT] and self.paddle.rect.right < WIDTH:
                self.paddle.rect.right += self.paddle.speed

            # update screen
            pygame.display.flip()
            self.clock.tick(self.fps)

    def show_menu(self):
        menu_background = pygame.image.load("images/back.jpg")
        menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

        rules_background = pygame.image.load("images/rules_background.jpg")
        rules_background = pygame.transform.scale(rules_background, (WIDTH, HEIGHT))

        rules = pygame.image.load("images/rules.png")
        rules = pygame.transform.scale(rules, (WIDTH, HEIGHT))

        buttons = [
            Button(890 * SCALE, 377 * SCALE, "Новая игра", 300, 100, (110, 110, 110)),
            Button(915 * SCALE, 477 * SCALE, "Правила", 300, 100, (110, 110, 110)),
            Button(920 * SCALE, 577 * SCALE, "Выход", 300, 100, (110, 110, 110))
        ]

        while self.is_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.sc.blit(menu_background, (0, 0))

            for ind, button in enumerate(buttons):
                if button.draw(self.sc):
                    if ind == 0:
                        self.is_menu = False
                        return True
                    if ind == 1:
                        while not pygame.key.get_pressed()[pygame.K_ESCAPE]:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    exit()

                            self.sc.blit(rules_background, (0, 0))
                            self.sc.blit(rules, (0, 0))

                            pygame.display.flip()
                            self.clock.tick(self.fps)
                    if ind == 2:
                        self.is_menu = False
                        return False

            # update screen
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    game = Game()
    game.run()
