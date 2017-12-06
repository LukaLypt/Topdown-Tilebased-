import pygame as pg
import random, sys
from os import path
from settings import *
from sprites import *
from tilemap import *

class Game:
    def __init__(self):
        pg.init()
        #pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        #pg.display.set_caption('GAME')
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.running = True
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map = Map(path.join(game_folder, 'map4.txt'))
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE,TILESIZE))

        #load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET_MOVE))
        self.spritesheet2 = Spritesheet(path.join(img_folder, SPRITESHEET_BOW))


    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))


    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                if sprite.health < 100:
                    sprite.draw_health()                          
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #after drawing everything on back of display, flip it over
        pg.display.flip()
            
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()


    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.run()
    g.show_go_screen()

pg.quit()
