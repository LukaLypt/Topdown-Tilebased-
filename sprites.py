import pygame as pg
from random import uniform
from settings import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2

class Spritesheet:
    #Utility class for loading and parsing Spritesheet
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        #grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        return image

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width /2
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width /2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height /2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height /2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.attacking = False
        self.direction = None
        self.reset_frame = None
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.south_frames[5]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0
        self.last_shot = 0

    def load_images(self):
        #MOVEMENT
        self.north_frames = [
        #self.game.spritesheet.get_image(0, 0, 64, 64),
        self.game.spritesheet.get_image(64, 0, 64, 64),
        self.game.spritesheet.get_image(128, 0, 64, 64),
        self.game.spritesheet.get_image(192, 0, 64, 64),
        self.game.spritesheet.get_image(256, 0, 64, 64),
        self.game.spritesheet.get_image(320, 0, 64, 64),
        self.game.spritesheet.get_image(384, 0, 64, 64),
        self.game.spritesheet.get_image(448, 0, 64, 64),
        self.game.spritesheet.get_image(512, 0, 64, 64)]
        for frame in self.north_frames:
            frame.set_colorkey(BLACK)
        self.west_frames = [
        self.game.spritesheet.get_image(0, 64, 64, 64),
        self.game.spritesheet.get_image(64, 64, 64, 64),
        self.game.spritesheet.get_image(128, 64, 64, 64),
        self.game.spritesheet.get_image(192, 64, 64, 64),
        self.game.spritesheet.get_image(256, 64, 64, 64),
        self.game.spritesheet.get_image(320, 64, 64, 64),
        self.game.spritesheet.get_image(384, 64, 64, 64),
        self.game.spritesheet.get_image(448, 64, 64, 64),
        self.game.spritesheet.get_image(512, 64, 64, 64)]
        for frame in self.west_frames:
            frame.set_colorkey(BLACK)
        self.south_frames = [
        #self.game.spritesheet.get_image(0, 128, 64, 64),
        self.game.spritesheet.get_image(64, 128, 64, 64),
        self.game.spritesheet.get_image(128, 128, 64, 64),
        self.game.spritesheet.get_image(192, 128, 64, 64),
        self.game.spritesheet.get_image(256, 128, 64, 64),
        self.game.spritesheet.get_image(320, 128, 64, 64),
        self.game.spritesheet.get_image(384, 128, 64, 64),
        self.game.spritesheet.get_image(448, 128, 64, 64),
        self.game.spritesheet.get_image(512, 128, 64, 64)]
        for frame in self.south_frames:
            frame.set_colorkey(BLACK)
        self.east_frames = [
        self.game.spritesheet.get_image(0, 192, 64, 64),
        self.game.spritesheet.get_image(64, 192, 64, 64),
        self.game.spritesheet.get_image(128, 192, 64, 64),
        self.game.spritesheet.get_image(192, 192, 64, 64),
        self.game.spritesheet.get_image(256, 192, 64, 64),
        self.game.spritesheet.get_image(320, 192, 64, 64),
        self.game.spritesheet.get_image(384, 192, 64, 64),
        self.game.spritesheet.get_image(448, 192, 64, 64),
        self.game.spritesheet.get_image(512, 192, 64, 64)]
        for frame in self.east_frames:
            frame.set_colorkey(BLACK)

        #ATTACKING -- CODE IS BREAKING GAME
        self.north_frames_bow = [
        self.game.spritesheet2.get_image(0, 0, 64, 64),
        self.game.spritesheet2.get_image(64, 0, 64, 64),
        self.game.spritesheet2.get_image(128, 0, 64, 64),
        self.game.spritesheet2.get_image(192, 0, 64, 64),
        self.game.spritesheet2.get_image(256, 0, 64, 64),
        self.game.spritesheet2.get_image(320, 0, 64, 64),
        self.game.spritesheet2.get_image(384, 0, 64, 64),
        self.game.spritesheet2.get_image(448, 0, 64, 64),
        self.game.spritesheet2.get_image(512, 0, 64, 64),
        self.game.spritesheet2.get_image(576, 0, 64, 64),
        self.game.spritesheet2.get_image(640, 0, 64, 64),
        self.game.spritesheet2.get_image(704, 0, 64, 64),
        self.game.spritesheet2.get_image(768, 0, 64, 64)]
        for frame in self.north_frames_bow:
            frame.set_colorkey(BLACK)
        self.west_frames_bow = [
        self.game.spritesheet2.get_image(0, 64, 64, 64),
        self.game.spritesheet2.get_image(64, 64, 64, 64),
        self.game.spritesheet2.get_image(128, 64, 64, 64),
        self.game.spritesheet2.get_image(192, 64, 64, 64),
        self.game.spritesheet2.get_image(256, 64, 64, 64),
        self.game.spritesheet2.get_image(320, 64, 64, 64),
        self.game.spritesheet2.get_image(384, 64, 64, 64),
        self.game.spritesheet2.get_image(448, 64, 64, 64),
        self.game.spritesheet2.get_image(512, 64, 64, 64),
        self.game.spritesheet2.get_image(576, 64, 64, 64),
        self.game.spritesheet2.get_image(640, 64, 64, 64),
        self.game.spritesheet2.get_image(704, 64, 64, 64),
        self.game.spritesheet2.get_image(768, 64, 64, 64)]
        for frame in self.west_frames_bow:
            frame.set_colorkey(BLACK)
        self.south_frames_bow = [
        self.game.spritesheet2.get_image(0, 128, 64, 64),
        self.game.spritesheet2.get_image(64, 128, 64, 64),
        self.game.spritesheet2.get_image(128, 128, 64, 64),
        self.game.spritesheet2.get_image(192, 128, 64, 64),
        self.game.spritesheet2.get_image(256, 128, 64, 64),
        self.game.spritesheet2.get_image(320, 128, 64, 64),
        self.game.spritesheet2.get_image(384, 128, 64, 64),
        self.game.spritesheet2.get_image(448, 128, 64, 64),
        self.game.spritesheet2.get_image(512, 128, 64, 64),
        self.game.spritesheet2.get_image(576, 128, 64, 64),
        self.game.spritesheet2.get_image(640, 128, 64, 64),
        self.game.spritesheet2.get_image(704, 128, 64, 64),
        self.game.spritesheet2.get_image(768, 128, 64, 64)]
        for frame in self.south_frames_bow:
            frame.set_colorkey(BLACK)
        self.east_frames_bow = [
        self.game.spritesheet2.get_image(0, 192, 64, 64),
        self.game.spritesheet2.get_image(64, 192, 64, 64),
        self.game.spritesheet2.get_image(128, 192, 64, 64),
        self.game.spritesheet2.get_image(192, 192, 64, 64),
        self.game.spritesheet2.get_image(256, 192, 64, 64),
        self.game.spritesheet2.get_image(320, 192, 64, 64),
        self.game.spritesheet2.get_image(384, 192, 64, 64),
        self.game.spritesheet2.get_image(448, 192, 64, 64),
        self.game.spritesheet2.get_image(512, 192, 64, 64),
        self.game.spritesheet2.get_image(576, 192, 64, 64),
        self.game.spritesheet2.get_image(640, 192, 64, 64),
        self.game.spritesheet2.get_image(704, 192, 64, 64),
        self.game.spritesheet2.get_image(768, 192, 64, 64)]
        for frame in self.east_frames_bow:
            frame.set_colorkey(BLACK)

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
            self.direction = 'north'
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
            self.direction = 'south'
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
            self.direction = 'west'
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
            self.direction = 'east'
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
        if keys[pg.K_SPACE]:
            self.attacking = True
            self.vel = vec(0, 0)
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                if self.direction == 'north':
                    dir = vec(0, -1).rotate(-self.rot)
                    b = Bullet(self.game, self.pos, dir)
                    b.image = pg.transform.rotate(b.image, 90)
                elif self.direction == 'south':
                    dir = vec(0, 1).rotate(-self.rot)
                    b = Bullet(self.game, self.pos, dir)
                    b.image = pg.transform.rotate(b.image, 270)
                elif self.direction == 'east':
                    dir = vec(1, 0).rotate(-self.rot)
                    b = Bullet(self.game, self.pos, dir)
                elif self.direction == 'west':
                    dir = vec(-1, 0).rotate(-self.rot)
                    b = Bullet(self.game, self.pos, dir)
                    b.image = pg.transform.rotate(b.image, 180)
                self.vel = vec(-KICKBACK, 0)


        elif not keys[pg.K_SPACE]:
            self.attacking = False

    def update(self):
        self.animate()
        self.get_keys()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls,'y')
        self.rect.center = self.hit_rect.center

        #Movement

    def animate(self):
        now = pg.time.get_ticks()
        #Movement down
        if self.vel.y > 0:
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.south_frames)
                self.image = self.south_frames[self.current_frame]
        #Attacking down
        elif self.attacking and self.direction == 'south':
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.south_frames_bow)
                self.image = self.south_frames_bow[self.current_frame]
        #Movement up
        elif self.vel.y < 0:
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.north_frames)
                self.image = self.north_frames[self.current_frame]
        #Attacking up
        elif self.attacking and self.direction == 'north':
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.north_frames_bow)
                self.image = self.north_frames_bow[self.current_frame]
        #Movement right
        elif self.vel.x > 0:
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.east_frames)
                self.image = self.east_frames[self.current_frame]
        #Attacking right
        elif self.attacking and self.direction == 'east':
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.east_frames_bow)
                self.image = self.east_frames_bow[self.current_frame]
        #Movement left
        elif self.vel.x < 0:
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.west_frames)
                self.image = self.west_frames[self.current_frame]
        #Attacking left
        elif self.attacking and self.direction == 'west':
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.west_frames_bow)
                self.image = self.west_frames_bow[self.current_frame]
        #Idle - Reset back to the first frame in the current frames of animation
        else:
            self.image = self.south_frames[5]


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        #self.rect = self.image.get_rect()
        self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()
        self.draw_health()

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.pos.x +=10
        self.rect.center = pos
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
