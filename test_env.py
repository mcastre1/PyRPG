import pygame as pg
from spriteSheet import *

pg.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("SpriteSheets")

BG = (50,50,50)
BLACK = (0, 0, 0)

sprite_sheet_image = pg.image.load('./img/char_right.png').convert_alpha()

sprite_sheet = SpriteSheet(sprite_sheet_image)

frame0 = sprite_sheet.get_image(0, 32, 32, 1, BLACK)
frame1 = sprite_sheet.get_image(1, 32, 32, 1, BLACK)
frame2 = sprite_sheet.get_image(2, 32, 32, 1, BLACK)

run = True
while run:

    # Update background
    screen.fill(BG)

    # Display image
    #screen.blit(sprite_sheet_image, (0,0))

    # Show frame image
    screen.blit(frame0, (0,0))
    screen.blit(frame1, (32,0))
    screen.blit(frame2, (64,0))

    # Check for events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.update()