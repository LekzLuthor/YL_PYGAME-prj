import pygame
from settings import *
from tile import Tile
from Player import Player


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # Sprites
        self.visible_sprites = pygame.sprite.Group()  # видимые спрайты
        self.obstacle_sprites = pygame.sprite.Group()  # спрайты вызывающие коллизии

        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    Player((x, y), [self.visible_sprites])

    def run(self):
        self.visible_sprites.draw(self.display_surface)
