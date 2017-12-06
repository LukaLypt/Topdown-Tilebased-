import pygame as pg

#define colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (180, 0, 0)
YELLOW = (255, 200, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 180)
DARKGREY = (78, 77, 83)
LIGHTGREY = (100,100,100)
BROWN = (106, 55, 5)

SPRITESHEET_MOVE = 'BODY_skeleton.png'
SPRITESHEET_BOW = 'BOW_skeleton.png'

#game options/settings
#TITLE = 'Tilemap'
WIDTH = 1024
HEIGHT = 768
FPS = 60
BGCOLOR = DARKGREY

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'tile1.png'

PLAYER_SPEED = 200
PLAYER_ROT_SPEED = 250
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)
#self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
#Gun settings
BULLET_IMG = 'arrow.png'
BULLET_SPEED = 500
BULLET_LIFETIME = 500
BULLET_RATE = 900
KICKBACK = 10
GUN_SPREAD = 5
BULLET_DAMAGE = 10
#BARREL_OFFSET = vec()

MOB_IMG = 'enemy1.png'
MOB_SPEED = 150
MOB_HIT_RECT = pg.Rect(0, 0, 35, 35)
MOB_HEALTH = 100
