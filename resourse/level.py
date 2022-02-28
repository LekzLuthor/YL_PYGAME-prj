import pygame
from settings import *
from tile import Tile
from Player import Player
from support import *
from debug_mode import debug
from weapon import Weapon
from ui import UI


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # Sprites
        self.visible_sprites = YSortCameraGroup()  # видимые спрайты
        self.obstacle_sprites = pygame.sprite.Group()  # спрайты вызывающие коллизии

        # attack sprites
        self.current_attack = None

        self.create_map()

        # interface
        self.ui = UI()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../map/main_game._block.csv'),
            'grass': import_csv_layout('../map/main_game._invisible_decoration.csv'),
            'object': import_csv_layout('../map/main_game._decoration.csv')
        }
        graphics = {
            # 'grass': import_folder('../textures/Grass'),
            'objects': import_folder('../textures/Objects'),
            'special_objects': import_folder('../textures/special')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites],
                                 'invisible')
                        if style == 'grass':
                            pass
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites],
                                 'object', surf)
                        if style == 'special_objects':
                            surf = graphics['special_objects'][int(col)]
                            Tile((x, y), [self.visible_sprites],
                                 'object', surf)

        self.player = Player(
            (1950, 450), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load('../textures/ground/main_map.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # getting offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
