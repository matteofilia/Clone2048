import pygame
from pygame.font import SysFont
from pygame.locals import *

from pygame.time import Clock

import random


class GameBoard:
    tiles = None

    def __init__(self):
        self.reset()
        random.seed()

    def reset(self):
        self.tiles = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

    def restart(self):
        self.reset()
        self.add_tile()
        self.add_tile()

    def slide_up(self):
        for x in range(0, 4, 1):
            for origin_y in range(0, 4, 1):
                y = origin_y
                while y > 0:
                    if self.tiles[x][y-1] == 0 or self.tiles[x][y-1] == self.tiles[x][origin_y]:
                        y -= 1
                    else:
                        break
                if y != origin_y:
                    if self.tiles[x][y] == 0:
                        self.tiles[x][y] = self.tiles[x][origin_y]
                        self.tiles[x][origin_y] = 0
                    else:
                        self.tiles[x][y] = self.tiles[x][origin_y]*2
                        self.tiles[x][origin_y] = 0

    def slide_down(self):
        for x in range(0, 4, 1):
            for origin_y in range(3, -1, -1):
                y = origin_y
                while y < 3:
                    if self.tiles[x][y+1] == 0 or self.tiles[x][y+1] == self.tiles[x][origin_y]:
                        y += 1
                    else:
                        break
                if y != origin_y:
                    if self.tiles[x][y] == 0:
                        self.tiles[x][y] = self.tiles[x][origin_y]
                        self.tiles[x][origin_y] = 0
                    else:
                        self.tiles[x][y] = self.tiles[x][origin_y] * 2
                        self.tiles[x][origin_y] = 0

    def slide_left(self):
        for y in range(0, 4, 1):
            for origin_x in range(0, 4, 1):
                x = origin_x
                while x > 0:
                    if self.tiles[x-1][y] == 0 or self.tiles[x-1][y] == self.tiles[origin_x][y]:
                        x -= 1
                    else:
                        break
                if x != origin_x:
                    if self.tiles[x][y] == 0:
                        self.tiles[x][y] = self.tiles[origin_x][y]
                        self.tiles[origin_x][y] = 0
                    else:
                        self.tiles[x][y] = self.tiles[origin_x][y] * 2
                        self.tiles[origin_x][y] = 0

    def slide_right(self):
        for y in range(0, 4, 1):
            for origin_x in range(3, -1, -1):
                x = origin_x
                while x < 3:
                    if self.tiles[x+1][y] == 0 or self.tiles[x+1][y] == self.tiles[origin_x][y]:
                        x += 1
                    else:
                        break
                if x != origin_x:
                    if self.tiles[x][y] == 0:
                        self.tiles[x][y] = self.tiles[origin_x][y]
                        self.tiles[origin_x][y] = 0
                    else:
                        self.tiles[x][y] = self.tiles[origin_x][y] * 2
                        self.tiles[origin_x][y] = 0

    def is_full(self):
        for y in self.tiles:
            for x in y:
                if x == 0:
                    return False
        return True

    def is_locked(self):
        if not self.is_full():
            return False

    def add_tile(self):
        if not self.is_full():
            while True:
                x = random.randint(0, 3)
                y = random.randint(0, 3)
                if self.tiles[x][y] == 0:
                    self.tiles[x][y] = 2
                    break

    def next(self):
        self.add_tile()

    def __str__(self):
        for y in self.tiles:
            for x in y:
                print(x, end=' ')
            print("\n", end='')


class GameBoardDrawer:
    DARK_WHITE = (247, 252, 252)
    BLACK = (0, 0, 0)
    DARK_GREY = (77, 77, 77)
    GREY = (105, 105, 105)
    LIGHT_GREY = (201, 201, 201)
    RED = (255, 0, 0)
    GREEN = (15, 255, 0)
    YELLOW = (235, 235, 52)
    PINK = (222, 31, 136)
    CYAN = (31, 219, 222)
    LIME = (111, 222, 31)
    PURPLE = (169, 34, 227)
    ORANGE = (222, 101, 31)
    TURQUOISE = (31, 222, 171)
    BROWN = (150, 87, 15)
    NAVY = (15, 44, 150)

    DEFAULT_TILE_SIZE = 128
    DEFAULT_TILE_WIDTH = 6
    DEFAULT_TILE_SPACING = 8

    def __init__(self):
        self.tile_font = None
        self.tile_font_colour = self.DARK_GREY
        self.tile_size = self.DEFAULT_TILE_SIZE
        self.tile_width = self.DEFAULT_TILE_WIDTH
        self.tile_spacing = self.DEFAULT_TILE_SPACING

    def init(self):
        # noinspection PyTypeChecker
        self.tile_font = SysFont(None, self.tile_size // 2)

    @classmethod
    def get_tile_colour(cls, val):
        if val == 0:
            return cls.LIGHT_GREY
        if val == 2:
            return cls.GREY
        if val == 4:
            return cls.YELLOW
        if val == 8:
            return cls.PINK
        if val == 16:
            return cls.CYAN
        if val == 32:
            return cls.LIME
        if val == 64:
            return cls.PURPLE
        if val == 128:
            return cls.ORANGE
        if val == 256:
            return cls.TURQUOISE
        if val == 512:
            return cls.RED
        if val == 1024:
            return cls.BROWN
        if val == 2048:
            return cls.NAVY
        if val == 4096:
            return cls.NAVY
        else:
            return cls.RED

    def draw_tiles(self, screen, tiles):
        for x in range(4):
            for y in range(4):
                self.draw_tile(screen, x, y, tiles[x][y])

    def draw_tile(self, screen, x, y, val):
        screen_width, screen_height = pygame.display.get_window_size()
        start_x = (screen_width - self.tile_size * 4 - self.tile_spacing * 3) // 2
        start_y = (screen_height - self.tile_size * 4 - self.tile_spacing * 3) // 2

        tile_x = start_x + x * self.tile_size + x * self.tile_spacing
        tile_y = start_y + y * self.tile_size + y * self.tile_spacing

        pygame.draw.rect(screen, self.get_tile_colour(val), (
            tile_x,
            tile_y,
            self.tile_size,
            self.tile_size),
            self.tile_width)

        text = self.tile_font.render(str(val), True, self.tile_font_colour)
        text_rect = text.get_rect()
        text_rect.left = tile_x + (self.tile_size - text_rect.width) // 2
        text_rect.top = tile_y + (self.tile_size - text_rect.height) // 2
        screen.blit(text, text_rect)

    def draw(self, screen, tiles):
        screen.fill(self.DARK_WHITE)
        self.draw_tiles(screen, tiles)


class Game:

    def __init__(self):
        self.running = True
        self.game_board = GameBoard()
        self.game_board_drawer = GameBoardDrawer()
        self.display = None
        self.clock = Clock()

    def check_game_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_w or event.key == K_UP:
                self.game_board.slide_up()
                self.game_board.next()
            if event.key == K_s or event.key == K_DOWN:
                self.game_board.slide_down()
                self.game_board.next()
            if event.key == K_a or event.key == K_LEFT:
                self.game_board.slide_left()
                self.game_board.next()
            if event.key == K_d or event.key == K_RIGHT:
                self.game_board.slide_right()
                self.game_board.next()

    def check_quit(self, event):
        if event.type == QUIT:
            self.running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            self.running = False

    def start(self):
        pygame.init()
        self.game_board_drawer.init()

        self.display = pygame.display.set_mode((720, 640))
        pygame.display.set_caption("Clone2048")

        self.game_board.restart()

        while self.running:
            self.game_board_drawer.draw(self.display, self.game_board.tiles)
            for event in pygame.event.get():
                self.check_quit(event)
                self.check_game_event(event)
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.start()
