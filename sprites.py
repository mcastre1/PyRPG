import pygame as pg
from settings import *
vec = pg.math.Vector2

from spriteSheet import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.next_move = pg.time.get_ticks() + 100
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.image = game.player_img
        #self.rect = self.image.get_rect()
        self.dx, self.dy = 0, 0
        self.x = x
        self.y = y
        self.next_move = pg.time.get_ticks()

        self.direction = "standing"
        sprite_sheet_image = pg.image.load('./img/char_right.png').convert_alpha()
        self.sprite_sheet = SpriteSheet(sprite_sheet_image)
        frame0 = self.sprite_sheet.get_image(0, 32, 32, 1, BLACK)
        self.image = frame0
        self.rect = self.image.get_rect()
        
        self.animation_list = []
        self.animation_steps = 3
        self.animation_cooldown = 50
        self.last_update = pg.time.get_ticks()
        self.frame = 0

        self.animate_sprite()

    def set_animation(self):
        pass


    def get_sprite_frame():
        pass
    
    def animate_sprite(self):
        for x in range(self.animation_steps):
            self.animation_list.append(self.sprite_sheet.get_image(x, 32, 32, 1, BLACK))

    def get_keys(self):
        self.dx, self.dy = 0, 0
        keys = pg.key.get_pressed()
        current_time = pg.time.get_ticks()

        if (keys[pg.K_UP] or keys[pg.K_w]) and (keys[pg.K_RIGHT] or keys[pg.K_d]):
            self.dy -= 1
            self.dx += 1
            self.direction = "diagonal"
        elif (keys[pg.K_UP] or keys[pg.K_w]) and (keys[pg.K_LEFT] or keys[pg.K_a]):
            self.dx -= 1
            self.dy -= 1
            self.direction = "diagonal"
        elif (keys[pg.K_DOWN] or keys[pg.K_s]) and (keys[pg.K_LEFT] or keys[pg.K_a]):
            self.dx -= 1
            self.dy += 1
            self.direction = "diagonal"
        elif (keys[pg.K_DOWN] or keys[pg.K_s]) and (keys[pg.K_RIGHT] or keys[pg.K_d]):
            self.dy += 1
            self.dx += 1
            self.direction = "diagonal"
        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            self.dx -= 1
            self.direction = "straight"
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.dx += 1
            self.direction = "straight"
            if current_time - self.last_update >= self.animation_cooldown:
                self.frame += 1
                self.last_update = current_time

                if self.frame >= len(self.animation_list):
                    self.frame = 0

                print(len(self.animation_list))
                print(self.frame)
                self.image = self.animation_list[self.frame]

                

        elif keys[pg.K_UP] or keys[pg.K_w]:
            self.dy -= 1
            self.direction = "straight"
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.dy += 1
            self.direction = "straight"
    
    def get_mv_exhaust(self, dir):
        if dir == 'straight':
            return int(STRAIGHT_MV_EXHAUST)
        elif dir == "diagonal":
            return int(DIAG_MV_EXHAUST)
        return 0


    def move(self, dx=0, dy=0):
        current_time = pg.time.get_ticks()

        if current_time - self.next_move >= 0:
            self.x += dx
            self.y += dy

            self.rect.x = self.x * TILESIZE
            self.collide_with_walls('x')
            self.rect.y = self.y * TILESIZE
            self.collide_with_walls('y')

            self.next_move = pg.time.get_ticks() + self.get_mv_exhaust(self.direction)

        
            
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.dx > 0:
                    self.x = hits[0].rect.left/32 - 1
                    self.rect.x = self.x * TILESIZE
                if self.dx < 0:
                    self.x = hits[0].rect.right/32
                    self.rect.x = self.x * TILESIZE
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.dy > 0:
                    self.y = hits[0].rect.top / 32 - 1
                    self.rect.y = self.y * TILESIZE
                if self.dy < 0:
                    self.y = hits[0].rect.bottom/32
                    self.rect.y = self.y * TILESIZE

    def update(self):
        self.get_keys()
        self.move(self.dx, self.dy)
        

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE