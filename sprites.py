import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.next_move = pg.time.get_ticks() + 100
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.dx, self.dy = 0, 0
        self.x = x
        self.y = y
    
    def get_keys(self):
        self.dx, self.dy = 0, 0
        keys = pg.key.get_pressed()

        if (keys[pg.K_UP] or keys[pg.K_w]) and (keys[pg.K_RIGHT] or keys[pg.K_d]):
            self.dy -= 1
            self.dx += 1
        elif (keys[pg.K_UP] or keys[pg.K_w]) and (keys[pg.K_LEFT] or keys[pg.K_a]):
            self.dx -= 1
            self.dy -= 1
        elif (keys[pg.K_DOWN] or keys[pg.K_s]) and (keys[pg.K_LEFT] or keys[pg.K_a]):
            self.dx -= 1
            self.dy += 1
        elif (keys[pg.K_DOWN] or keys[pg.K_s]) and (keys[pg.K_RIGHT] or keys[pg.K_d]):
            self.dy += 1
            self.dx += 1
        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            self.dx -= 1
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.dx += 1
        elif keys[pg.K_UP] or keys[pg.K_w]:
            self.dy -= 1
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.dy += 1
        
    def set_next_move(self, tick=0):
            self.next_move = pg.time.get_ticks() + tick

    def move(self, dx=0, dy=0):
        if pg.time.get_ticks() >= self.next_move: 
        
            self.x += dx
            self.y += dy

            # Ticking down movement depending on vertical or diagonal movement.
            if not dx == 0 and not dy == 0:  # Diagonal movement
                self.next_move = pg.time.get_ticks() + 200
            else:                            # Vertical movement
                self.next_move = pg.time.get_ticks() + 100
            
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
        self.rect.x = self.x * TILESIZE
        self.collide_with_walls('x')
        

        self.rect.y = self.y * TILESIZE
        self.collide_with_walls('y')
        

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