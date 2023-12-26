
from board import boards
import pygame
import math



# initialize pygame
pygame.init()


WIDTH = 900
HEIGHT = 950
LEVEL = 0
COLOR = 'blue'
PI = math.pi

# screen object?
screen = pygame.display.set_mode([WIDTH, HEIGHT])

timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20) # font family and size



def draw_board(scrn, lvl, clr):
    tilesX = (WIDTH // 30)
    tilesY = ((HEIGHT - 50) // 32) # why "- 50"??

    for y, row in enumerate(lvl):
        for x, val in enumerate(row):
            if val == 1: 
                ''' SMALL CIRCLE  '''
                pygame.draw.circle(
                    scrn,
                    'white',
                    (
                        x*tilesX + 0.5*tilesX,
                        y*tilesY + 0.5*tilesY
                    ),
                    4 # doe some math for this instead?? not just hard code??
                )
            elif val == 2:
                ''' BIG CIRCLE'''
                pygame.draw.circle(
                    scrn,
                    'white',
                    (
                        x*tilesX + 0.5*tilesX,
                        y*tilesY + 0.5*tilesY
                    ),
                    10
                )                
            elif val == 3:
                ''' COLORED VERTICLE LINE '''
                pygame.draw.line(
                    scrn, clr, 
                    (
                        x*tilesX + 0.5*tilesX,
                        y*tilesY
                    ),
                    (
                        x*tilesX + 0.5*tilesX,
                        y*tilesY + tilesY
                    ), 3
                )                                        
            elif val == 4:
                ''' COLORED HORIZONTAL LINE '''
                pygame.draw.line(
                    scrn, clr, 
                    (
                        x*tilesX,
                        y*tilesY + 0.5*tilesY
                    ),
                    (
                        x*tilesX + tilesX,
                        y*tilesY + 0.5*tilesY
                    ), 3
                )  
            elif val == 5:
                pygame.draw.arc(
                    scrn, clr, 
                    [(x*tilesX - tilesX*.4) - 2, (y*tilesY + .5*tilesY), tilesX, tilesY],
                    0, PI/2, 3
                )
            elif val == 6:
                pygame.draw.arc(
                    scrn, clr, 
                    [(x*tilesX + tilesX*.5), (y*tilesY + .5*tilesY), tilesX, tilesY],
                    PI/2, PI, 3
                )
            elif val == 7:
                pygame.draw.arc(
                    scrn, clr, 
                    [(x*tilesX + tilesX*.5), (y*tilesY - .4*tilesY), tilesX, tilesY],
                    PI, 3*PI/2, 3
                )
            elif val == 8:
                pygame.draw.arc(
                    scrn, clr, 
                    [(x*tilesX - tilesX*.4) - 2, (y*tilesY - .4*tilesY), tilesX, tilesY],
                    3*PI/2, 2*PI, 3
                )
            elif val == 9:
                ''' WHITE HORIZONTAL LINE (for ghosts) '''
                pygame.draw.line(
                    scrn, 'white', 
                    (
                        x*tilesX,
                        y*tilesY + 0.5*tilesY
                    ),
                    (
                        x*tilesX + tilesX,
                        y*tilesY + 0.5*tilesY
                    ), 3
                )  



run = True

# game loop... similar to render loop in like OpenGL?
while run:
    timer.tick(fps) # tick by seconds based on fps??
    screen.fill('black') # black background

    draw_board(screen, boards[LEVEL], COLOR) # draw board based on board level

    # anything pygame can process (i.e. mouse click?) is handled in "event.get()"??
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # when click red "x" in window 
            run = False

    pygame.display.flip() # is it because display inverted (such as in cairo)? OR is it simply just to draw in screen every iteration??

pygame.quit() # quit window once out of game loop