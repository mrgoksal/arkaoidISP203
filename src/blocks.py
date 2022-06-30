from configs import *
from random import randrange as rnd


class Blocks:
    def __init__(self):
        # Создание массива блоков и рандомных цветов для него
        self.block_list = [pygame.Rect(60 + (BLOCKS_WIDTH + BLOCKS_DIST) * i, 60 + (BLOCKS_HEIGHT + BLOCKS_DIST) * j, BLOCKS_WIDTH, BLOCKS_HEIGHT) for i in range(BLOCKS_COUNT) for j in range(4)]
        self.color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(BLOCKS_COUNT) for j in range(4)]
