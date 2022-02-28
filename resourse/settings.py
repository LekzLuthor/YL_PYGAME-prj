# game settings
WIDTH = 1440
HEIGHT = 720
FPS = 60
TILE_SIZE = 64
BACKGROUND_COLOR = (184, 220, 229)

# weapons
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': '../textures/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30, 'graphic': '../textures/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': '../textures/weapons/axe/full.png'},
    'rapier': {'cooldown': 50, 'damage': 8, 'graphic': '../textures/weapons/rapier/full.png'},
    'sai': {'cooldown': 80, 'damage': 10, 'graphic': '../textures/weapons/sai/full.png'}}

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../textures/font/stix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = (156, 10, 10)
ENERGY_COLOR = (244, 169, 4)
UI_BORDER_COLOR_ACTIVE = 'gold'
