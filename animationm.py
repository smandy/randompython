from typing import Sequence, Dict, cast

import pygame
import sys
import time

# from pygame import QUIT
# set up pygame
pygame.init()

# set up the window
WINDOWWIDTH = 400
WINDOWHEIGHT = 400
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Animation')

# set up direction variables
DOWNLEFT = 1
DOWNRIGHT = 3
UPLEFT = 7
UPRIGHT = 9

MOVESPEED = 4

# set up the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set up the block data structure
b1 = {'rect': pygame.Rect(300, 80, 50, 100), 'color': RED, 'dir': UPRIGHT}
b2 = {'rect': pygame.Rect(200, 200, 20, 20), 'color': GREEN, 'dir': UPLEFT}
b3 = {'rect': pygame.Rect(100, 150, 60, 60), 'color': BLUE, 'dir': DOWNLEFT}
blocks: Sequence[Dict[str, object]] = [b1, b2, b3]

# run the game loop
while True:
    # check for the QUIT event
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # draw the black background onto the surface
    windowSurface.fill(BLACK)

    for b in blocks:
        # move the block data structure

        rect: pygame.Rect = cast(pygame.Rect, b['rect'])
        color: pygame.Color = cast(pygame.Color, b['color'])
        if b['dir'] == DOWNLEFT:
            rect.left -= MOVESPEED
            rect.top += MOVESPEED
        if b['dir'] == DOWNRIGHT:
            rect.left += MOVESPEED
            rect.top += MOVESPEED
        if b['dir'] == UPLEFT:
            rect.left -= MOVESPEED
            rect.top -= MOVESPEED
        if b['dir'] == UPRIGHT:
            rect.left += MOVESPEED
            rect.top -= MOVESPEED

        # check if the block has move out of the window
        if rect.top < 0:
            # block has moved past the top
            if b['dir'] == UPLEFT:
                b['dir'] = DOWNLEFT
            if b['dir'] == UPRIGHT:
                b['dir'] = DOWNRIGHT
        if rect.bottom > WINDOWHEIGHT:
            # block has moved past the bottom
            if b['dir'] == DOWNLEFT:
                b['dir'] = UPLEFT
            if b['dir'] == DOWNRIGHT:
                b['dir'] = UPRIGHT
        if rect.left < 0:
            # block has moved past the left side
            if b['dir'] == DOWNLEFT:
                b['dir'] = DOWNRIGHT
            if b['dir'] == UPLEFT:
                b['dir'] = UPRIGHT
        if rect.right > WINDOWWIDTH:
            # block has moved past the right side
            if b['dir'] == DOWNRIGHT:
                b['dir'] = DOWNLEFT
            if b['dir'] == UPRIGHT:
                b['dir'] = UPLEFT

        # draw the block onto the surface
        pygame.draw.rect(windowSurface, color, rect)

    # draw the window onto the screen
    pygame.display.update()
    time.sleep(0.02)
