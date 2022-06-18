import pygame
from random import randrange as rnd

# Настройки окна
WIDTH = 1920  # Ширина
HEIGHT = 1080  # Высота
SCALE = WIDTH / 1920  # Коэффициент скейла
FPS = 60  # Тикрейт (частота спроса)

# Настройки "отбивной" доски
PADDLE_W = 330  # Ширина
PADDLE_H = 35  # Высота
PADDLE_SPEED = 15  # Скорость перемещения

# Настройки мяча
BALL_RADIUS = 20  # Радиус
BALL_SPEED = 6  # Скорость полета

# Настройки  блоков
BLOCKS_WIDTH = 192  # Ширина
BLOCKS_HEIGHT = 50  # Высота
BLOCKS_DIST = 20  # Интервал между блоками
BLOCKS_LENGTH = BLOCKS_WIDTH + BLOCKS_DIST  # Расчет длины одного блока
BLOCKS_COUNT = WIDTH // BLOCKS_LENGTH  # Расчет количества блоков на экране

# Настройки кнопок
BUTTON_W = 300  # Ширина
BUTTON_H = 100  # Высота
