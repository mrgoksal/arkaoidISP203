# Импорт ресуров
from configs import *
from src.ball import Ball
from src.blocks import Blocks
from src.button import Button
from src.paddle import Paddle


class Game:
    # Инициализация окна и игровых элементов
    def __init__(self):
        self.img = None
        self.clock = None
        self.sc = None
        self.fps = FPS
        self.width = WIDTH
        self.height = HEIGHT

        # Меню
        self.is_menu = True

        # Мяч
        self.ball = Ball()

        # Отбивная "доска"
        self.paddle = Paddle()

        # Блоки
        self.blocks = Blocks()

    #  Первичный запуск + программный цикл
    def run(self):
        pygame.init()  # Инициализация pygame
        # Настройка разрешения окна
        self.sc = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # Фоновое изображение (подгрузка + скейл)
        self.img = pygame.image.load('images/background.jpg').convert()
        self.img = pygame.transform.scale(self.img, (WIDTH, HEIGHT))

        # Программный цикл
        while True:
            if not self.show_menu():
                return
            self.game_loop()

    # Обнуление программных констант (возвращение в меню + пересоздание элементов)
    def restart(self):
        self.is_menu = True
        self.ball = Ball()
        self.paddle = Paddle()
        self.blocks = Blocks()

    # Обнаружение коллизии путем сравнения координат + нормализация положения мяча
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

    # Функция заупска игрового цикла
    def game_loop(self):
        while not self.is_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            self.sc.blit(self.img, (0, 0))

            # Отрисовка блоков
            [pygame.draw.rect(self.sc, self.blocks.color_list[color], block) for color, block in
             enumerate(self.blocks.block_list)]

            # Отрисовка "отбивочной доски"
            pygame.draw.rect(self.sc, pygame.Color('darkorange'), self.paddle)

            # Отрисовка мяча
            pygame.draw.circle(self.sc, pygame.Color('white'), self.ball.rect.center, self.ball.radius)

            # Расчет смещения мяча скорость*метровое смещение
            self.ball.rect.x += self.ball.speed * self.ball.dx
            self.ball.rect.y += self.ball.speed * self.ball.dy

            # Нормализация положения мяча при касании оным одного из краев (левого или правого) (угол вхождения = углу выхождения)
            if self.ball.rect.centerx < self.ball.radius or self.ball.rect.centerx > WIDTH - self.ball.radius:
                self.ball.dx = -self.ball.dx

            # Нормализация положения мяча при касании оным верхнего края экрана
            if self.ball.rect.centery < self.ball.radius:
                self.ball.dy = -self.ball.dy

            # Расчет положения мяча при касании оным "отбивочной" доски
            if self.ball.rect.colliderect(self.paddle) and self.ball.dy > 0:
                self.ball.dx, self.ball.dy = self.detect_collision()

            # Расчет положения мяча при касании оного с блоком с удалением последнего
            hit_index = self.ball.rect.collidelist(self.blocks.block_list)
            if hit_index != -1:
                hit_rect = self.blocks.block_list.pop(hit_index)
                hit_color = self.blocks.color_list.pop(hit_index)
                self.ball.dx, self.ball.dy = self.detect_collision()

                # Специальный эффект при уничтожении блока
                hit_rect.inflate_ip(self.ball.rect.width * 3, self.ball.rect.height * 3)
                pygame.draw.rect(self.sc, hit_color, hit_rect)
                self.fps += 2

            # Конец игры. Условие поражения (положение мяча < высоты экрана) и  условие победы (список блоков пуст)
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
        # Подгрузка и скейл фоновых изображений для различных экранных форм
        menu_background = pygame.image.load("images/back.jpg")
        menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

        rules_background = pygame.image.load("images/rules_background.jpg")
        rules_background = pygame.transform.scale(rules_background, (WIDTH, HEIGHT))

        rules = pygame.image.load("images/rules.png")
        rules = pygame.transform.scale(rules, (WIDTH, HEIGHT))

        # Инициализация кнопок (oX, oY, текст внутри, ширина кликабельной области, высота кликабельной области, цвет выделения)
        buttons = [
            Button(895 * SCALE, 350 * SCALE, "Новая игра", 300, 100, (110, 110, 110)),
            Button(910 * SCALE, 450 * SCALE, "Правила", 300, 100, (110, 110, 110)),
            Button(920 * SCALE, 550 * SCALE, "Выход", 300, 100, (110, 110, 110))
        ]

        # Цикл меню
        while self.is_menu:
            # Считывание взаимодействий пользователя с программой (за тик)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            # Отрисовка фона
            self.sc.blit(menu_background, (0, 0))
            # Добавление "эффекта" от наведения+нажатия на кнопку
            for ind, button in enumerate(buttons):
                if button.draw(self.sc):
                    # Новая игра
                    if ind == 0:
                        self.is_menu = False  # Прекращение цикла меню
                        return True
                    if ind == 1:
                        # Запуск экрана правил
                        # Считывание взаимодействий пользователя с программой
                        while not pygame.key.get_pressed()[pygame.K_ESCAPE]:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    exit()

                            # Отрисовка фона и текста правил
                            self.sc.blit(rules_background, (0, 0))
                            self.sc.blit(rules, (0, 0))
                            # Обнвление дисплея (переход на следующий тик) + установка тикрейта
                            pygame.display.flip()
                            self.clock.tick(self.fps)
                    if ind == 2:
                        # Выход из программы (прекращение программного цикла)
                        self.is_menu = False
                        return False

            # Обновление дисплея (переход на следующий тик) + установка тикрейта
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    game = Game()
    game.run()
