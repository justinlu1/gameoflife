import pygame, sys
from copy import copy, deepcopy

# initialize pygame
pygame.init()  


# Constants
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
GAME_FONT = pygame.freetype.SysFont("Calibri", 18)
TITLE_FONT = pygame.freetype.SysFont("Calibri", 30)
screen = pygame.display.set_mode([WINDOW_HEIGHT, WINDOW_WIDTH])

NUM_ROWS = 50
NUM_COLS = 50

PIXEL_SIZE = WINDOW_HEIGHT // NUM_ROWS

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (128, 128, 128)

GAME_FPS = 60
running = True


# program loop
while running == True:
    # setting variables
    board = [[False] * NUM_ROWS for i in range(NUM_COLS)]

    clock = pygame.time.Clock()
    clock.tick(GAME_FPS)

    frame = 1
    speed = 50
    generation = 0
    
    startmenu = True
    setup = True
    simulation = True

    # start menu
    while startmenu == True:
        screen.fill(COLOR_BLACK)

        TITLE_FONT.render_to(screen, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 50), "Conway's Game of Life", (255, 255, 255))

        starttext = "Click to start"
        GAME_FONT.render_to(screen, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2), starttext, (255, 255, 255))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                    startmenu = False

    # set up the board
    while setup == True:
        clock.tick(GAME_FPS)
        # text
        screen.fill(COLOR_BLACK)

        title = "Click on a tile to place a cell."
        GAME_FONT.render_to(screen, (5, 5), title, COLOR_WHITE)

        # user inputs 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] < WINDOW_WIDTH and pos[1] < WINDOW_HEIGHT:
                    # print(str(pos))
                    x = pos[0] // PIXEL_SIZE
                    y = pos[1] // PIXEL_SIZE
                    board[x][y] = not board[x][y]
                    #print("clicked at " + str(pos) + ", stored in " + str(x) + ", " + str(y))
                # draw board as the player clicks

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    setup = False

        # shade under mouse
        pos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, COLOR_GRAY, pygame.Rect(pos[0] - (pos[0] % PIXEL_SIZE), 
                                                            pos[1] - (pos[1] % PIXEL_SIZE), PIXEL_SIZE, PIXEL_SIZE))

        # draw tiles
        for row in range(0, NUM_ROWS):
            for col in range(0, NUM_COLS):
                #print(str(row) + ", " + str(col) + " is " + str(board[row][col]))
                if board[row][col] == True:
                    #print("Found clicked tile, drawing at " + str(row * 4) + ", " + str(col * 4))
                    pygame.draw.rect(screen, COLOR_WHITE, pygame.Rect(
                        row * PIXEL_SIZE, col * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
        pygame.display.update()

    # simulation loop
    while simulation == True:
        clock.tick(GAME_FPS)
        print(speed)
        frame += 1
        
        # take inputs
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_UP] and speed < 100:
                    speed += 1

            if keys[pygame.K_DOWN] and speed > 0:
                    speed -= 1

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    simulation = False

                if event.key == pygame.K_ESCAPE:
                    simulation = False
                    running = False

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # update board
        if speed == 0:
            freeze = True
            while freeze == True:
                keys = pygame.key.get_pressed()
                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_UP] and speed < 100:
                            speed += 1
                            freeze = False
                            
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            simulation = False

                        if event.key == pygame.K_ESCAPE:
                            simulation = False
                            running = False
                        freeze = False

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

        if frame % (101 - speed) == 0:
            generation += 1
            temp = deepcopy(board);

            for x in range(0, NUM_ROWS):
                for y in range(0, NUM_COLS):
                    neighbors = 0

                    # find neighbors
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i == 0 and j == 0:
                                continue
                            if x + i >= NUM_ROWS or y + j >= NUM_COLS:
                                break
                            if board[x + i][y + j] == True:
                                neighbors += 1

                    # determine life or death
                    #print(str(x) + ", " + str(y) + " has " + str(neighbors) + " neighbors")
                    if board[x][y] == True:
                        if neighbors < 2 or neighbors > 3:
                            #print("death at " + str(x) + ", " + str(y))
                            temp[x][y] = False
                        else: 
                            temp[x][y] = True

                    if board[x][y] == False:
                        if neighbors == 3:
                            #print("birth at " + str(x) + ", " + str(y))
                            temp[x][y] = True
                        else:
                            temp[x][y] = False
            board = temp;

        screen.fill(COLOR_BLACK)

        # text
        GAME_FONT.render_to(screen, (5, 770), "ESC to quit, r to restart, UP arrow to speed up, DOWN arrow to slow down", COLOR_WHITE)

        speedText = "speed: " + str(speed * 2) + "%"
        GAME_FONT.render_to(screen, (5, 750), speedText, COLOR_WHITE)

        generationText = "generation: " + str(generation)
        GAME_FONT.render_to(screen, (5, 730), generationText, COLOR_WHITE)

        for row in range(0, NUM_ROWS):
            for col in range(0, NUM_COLS):
                #print(str(row) + ", " + str(col) + " is " + str(board[row][col]))
                if board[row][col] == True:
                    #print("Found clicked tile, drawing at " + str(row * 4) + ", " + str(col * 4))
                    pygame.draw.rect(screen, COLOR_WHITE, pygame.Rect(
                    row * PIXEL_SIZE, col * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
        pygame.display.update()
