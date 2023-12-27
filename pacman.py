
from board import boards
import pygame
import math


def bool_swap(val):
    if val is True: return False
    elif val is False: return True



# initialize pygame
pygame.init()


WIDTH = 900
HEIGHT = 950
LEVEL = 0
BOARD = boards[LEVEL]
COLOR = 'blue'
PI = math.pi


RIGHT, UP, LEFT, DOWN = 0, 1, 2, 3

# screen object?
screen = pygame.display.set_mode([WIDTH, HEIGHT])

timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20) # font family and size


player_images = []

player_image_frames = 5 # hold each image for this amount of frames
big_dot_flicker_frames = 10 # hold toggled flicker for this amout of frames


# RIGHT, UP, LEFT, DOWN
turns_allowed = [False, False, False, False] # are we allowed to turn in these directions
direction_command = RIGHT



for i in range(1, 5):
    player_images.append(
        pygame.transform.scale(
            pygame.image.load(f'assets/player_images/{i}.png'),
            (45, 45)
        )
    )


# start tiles?? he did guess and check...
# basically position coordinates for player, initialized to start position
player_x = 450
player_y = 663

direction = RIGHT
counter_player = 0
counter_big_dot_flicker = 0
big_dot_flicker = False
player_speed = 2


def draw_board(scrn, brd, clr):
    tilesX = (WIDTH // 30)
    tilesY = ((HEIGHT - 50) // 32) # why "- 50"??

    for y, row in enumerate(brd):
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
            elif val == 2 and big_dot_flicker:
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



def draw_player(img_ind): 

    blit_player_img = player_images[img_ind] # to cycle through each of 4 images?? ...since counter increments...

    if direction == RIGHT: pass
    elif direction == UP: blit_player_img = pygame.transform.rotate(blit_player_img, 90)
    elif direction == LEFT: blit_player_img = pygame.transform.rotate(blit_player_img, 180)
    elif direction == DOWN: blit_player_img = pygame.transform.rotate(blit_player_img, 270)

    screen.blit(blit_player_img, (player_x, player_y))



def check_position(cx, cy, brd):
    turns = [False, False, False, False]

    tilesX = (WIDTH // 30)
    tilesY = ((HEIGHT - 50) // 32) # why "- 50"??

    margin = 15 # margin??

    # check collisions based on center x and center y of player +/- fudge factor (margin)
    if cx//30 < 29:


        if direction == RIGHT:
            if brd[cy//tilesY][(cx-margin)//tilesX] < 3: turns[LEFT] = True
        elif direction == UP:
            if brd[(cy+margin)//tilesY][cx//tilesX] < 3: turns[DOWN] = True                
        elif direction == LEFT:
            if brd[cy//tilesY][(cx+margin)//tilesX] < 3: turns[RIGHT] = True
        elif direction == DOWN:
            if brd[(cy-margin)//tilesY][cx//tilesX] < 3: turns[UP] = True                

        if direction == UP or direction == DOWN:
            if 12 <= cx % tilesX <= 18: # checking if roughly at midpoint of tile...
                if brd[(cy + margin)//tilesY][cx//tilesX] < 3: turns[DOWN] = True    
                elif brd[(cy - margin)//tilesY][cx//tilesX] < 3: turns[UP] = True                               
            if 12 <= cy % tilesY <= 18: # checking if roughly at midpoint of tile...
                if brd[cy//tilesY][(cx-tilesX)//tilesX] < 3: turns[LEFT] = True    
                elif brd[cy//tilesY][(cx+tilesX)//tilesX] < 3: turns[RIGHT] = True  


        if direction == RIGHT or direction == LEFT:
            if 12 <= cx % tilesX <= 18: # checking if roughly at midpoint of tile...
                if brd[(cy + tilesY)//tilesY][cx//tilesX] < 3: turns[DOWN] = True    
                elif brd[(cy - tilesY)//tilesY][cx//tilesX] < 3: turns[UP] = True                               
            if 12 <= cy % tilesY <= 18: # checking if roughly at midpoint of tile...
                if brd[cy//tilesY][(cx-margin)//tilesX] < 3: turns[LEFT] = True    
                elif brd[cy//tilesY][(cx+margin)//tilesX] < 3: turns[RIGHT] = True  



    else:
        turns[0] = True
        turns[1] = True


    return turns


def move_player(play_x, play_y):
    if direction == RIGHT and turns_allowed[RIGHT]: play_x += player_speed
    elif direction == UP and turns_allowed[UP]: play_y += player_speed
    elif direction == LEFT and turns_allowed[LEFT]: play_x -= player_speed
    elif direction == DOWN and turns_allowed[DOWN]: play_y -= player_speed
    return play_x, play_y


player_x, player_y = move_player(player_x, player_y)

run = True

# game loop... similar to render loop in like OpenGL?
while run:
    timer.tick(fps) # tick by seconds based on fps??

    

    if counter_player < int(player_image_frames*4): # why??
        player_image_index = counter_player // player_image_frames
        counter_player += 1
    else: counter_player = 0

    if counter_big_dot_flicker < big_dot_flicker_frames: counter_big_dot_flicker += 1
    else: 
        big_dot_flicker = bool_swap(big_dot_flicker)
        counter_big_dot_flicker = 0         


    screen.fill('black') # black background

    draw_board(screen, BOARD, COLOR) # draw board based on board level
    draw_player(player_image_index)


    # center_x, center_y = None, None
    # turns_allowed = check_position(center_x, center_y, BOARD)

    # anything pygame can process (i.e. mouse click?) is handled in "event.get()"??
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # when click red "x" in window 
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT: direction_command = RIGHT
            elif event.key == pygame.K_UP: direction_command = UP
            elif event.key == pygame.K_LEFT: direction_command = LEFT
            elif event.key == pygame.K_DOWN: direction_command = DOWN
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == RIGHT: direction_command = direction
            elif event.key == pygame.K_UP and direction_command == UP: direction_command = direction
            elif event.key == pygame.K_LEFT and direction_command == LEFT: direction_command = direction
            elif event.key == pygame.K_DOWN and direction_command == DOWN: direction_command = direction

        for dir in range(4):
            if direction_command == dir and turns_allowed[dir]:
                direction = dir


        # keeping within boundaries
        if player_x > 900:
            player_x = -47 # all the way to left?
        elif player_x < -50:
            player_x = 84 # all the way to the right?


    pygame.display.flip() # is it because display inverted (such as in cairo)? OR is it simply just to draw in screen every iteration??

pygame.quit() # quit window once out of game loop