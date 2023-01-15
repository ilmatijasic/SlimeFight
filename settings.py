import math

# game settings
WIDTH, HEIGHT = 1600, 900
RES = WIDTH, HEIGHT
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60

INIT_PLAYER_POS = HALF_WIDTH, HALF_HEIGHT

PLAYER_SPEED = 5/16
PLAYER_SIZE_SCALE = 2
PLAYER_MAX_HEALTH = 100
PLAYER_ANIMATION_SPEED = 1/10
PLAYER_DIAGONAL_SPEED_REDUCTION = math.sqrt(2)

PLAYER_MAX_HEALTH = 100
PLAYER_HEALTH_BAR_PADDING = 5
PLAYER_HEALTH_BAR_X = WIDTH - 200
PLAYER_HEALTH_BAR_Y = HEIGHT - 100
PLAYER_HEALTH_BAR_WIDTH = 100
PLAYER_HEALTH_BAR_HEIGHT = 30

PLAYER_STATS_WIDTH = 200
PLAYER_STATS_HEIGHT = 200
PLAYER_STATS_X = 25
PLAYER_STATS_Y = HEIGHT - PLAYER_STATS_HEIGHT - PLAYER_STATS_X

BULLET_SPEED = 15 / 16
BULLET_DAMAGE = 10
TIME_BETWEEN_SHOTS = 100
MAX_TIME_BETWEEN_SHOTS = TIME_BETWEEN_SHOTS // 2

SLIME_SIZE_SCALE = 2
SLIME_SPEED = 1/16
SLIME_OFFSET = 80
SLIME_OFFSET_RESET = 180
SLIME_ANIMATION_SPEED = 1/10
SLIME_DAMAGE = 4
SLIME_MAX_HEALTH = 100

MAX_MOBS = 10


MAP_PATH = "Assets\map\TX Tileset Grass.png"
MAP_WALL_PATH = "Assets\map\TX Tileset Wall.png"

FONT = 'calibri.ttf'
FONT_SIZE = 30


