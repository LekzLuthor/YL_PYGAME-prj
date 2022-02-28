from Player import Player
from enemy import Enemy
from settings import *
from support import *
from tile import Tile
from ui import UI
from weapon import Weapon
from random import choice


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # Sprites
        self.visible_sprites = YSortCameraGroup()  # видимые спрайты
        self.obstacle_sprites = pygame.sprite.Group()  # спрайты вызывающие коллизии

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.create_map()

        # interface
        self.ui = UI()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../map/main_game._block.csv'),
            'grass': import_csv_layout('../map/main_game._place_holders_ff.csv'),
            'object': import_csv_layout('../map/main_game._decoration.csv'),
            'entities': import_csv_layout('../map/main_game._Entitles.csv')
        }
        graphics = {
            'grass': import_folder('../textures/grass'),
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
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                                 'grass', random_grass_image)
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites],
                                 'object', surf)
                        if style == 'special_objects':
                            surf = graphics['special_objects'][int(col)]
                            Tile((x, y), [self.visible_sprites],
                                 'object', surf)
                        if style == 'entities':
                            if col == '0':
                                self.player = Player(
                                    (x + 25, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic
                                )
                            else:
                                if col == '1':
                                    monster_name = 'bamboo'
                                elif col == '2':
                                    monster_name = 'raccoon'
                                elif col == '3':
                                    monster_name = 'spirit'
                                elif col == '4':
                                    monster_name = 'squid'

                                Enemy(monster_name, (x, y),
                                      [self.attackable_sprites, self.visible_sprites],
                                      self.obstacle_sprites,
                                      self.damage_player)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        pass

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
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

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
