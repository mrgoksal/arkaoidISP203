import pygame
from random import randrange as rnd

# game settings
WIDTH = 1600
HEIGHT = 900
SCALE = WIDTH / 1920
FPS = 60

# paddle settings
PADDLE_W = 330
PADDLE_H = 15
PADDLE_SPEED = 20

# ball settings
BALL_RADIUS = 10
BALL_SPEED = 6

# blocks settings
BLOCKS_WIDTH = 100
BLOCKS_HEIGHT = 25
BLOCKS_DIST = 20
BLOCKS_LENGTH = BLOCKS_WIDTH + BLOCKS_DIST
BLOCKS_COUNT = WIDTH // BLOCKS_LENGTH

# buttons settings
BUTTON_W = 300
BUTTON_H = 100
