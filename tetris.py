import pygame
import random

# constants
BLOCK_SIZE = 30
GRID_WIDTH = 300  # 10 by 20 grid
GRID_HEIGHT = 600
WIDTH = 700  # pygame window dimensions
HEIGHT = 700

# coordinates of grid at top left corner
X_GRID = (WIDTH - GRID_WIDTH) // 3  # grid is in the middle
Y_GRID = HEIGHT - GRID_HEIGHT  # grid is along the bottom

# shapes
class Shape(object):
    def __init__(self, x, y):
        self.x = x # start at middle of grid
        self.y = y # start at top of grid
        self.rotation = 0 # initial rotation state
        self.orig_x = x
        self.orig_y = y

    def reset(self):
        self.x = self.orig_x
        self.y = self.orig_y
        self.rotation = 0

class OShape(Shape):
    def __init__(self):
        Shape.__init__(self, 4, -2)
        self.state1 = [[1,1],
                       [1,1]]
        self.states = [self.state1]
        self.colour = (255, 255, 0)

class IShape(Shape):
    def __init__(self):
        Shape.__init__(self, 4, -4)
        self.state1 = [[1],
                       [1],
                       [1],
                       [1]]
        self.state2 = [[1,1,1,1]]
        self.states = [self.state1, self.state2]
        self.colour = (0, 255, 255)

class TShape(Shape):
    def __init__(self):
        Shape.__init__(self, 4, -2)
        self.state1 = [[1,1,1],
                       [0,1,0]]
        self.state2 = [[1,0],
                       [1,1],
                       [1,0]]
        self.state3 = [[0,1,0],
                       [1,1,1]]
        self.state4 = [[0,1],
                       [1,1],
                       [0,1]]
        self.states = [self.state1, self.state2, self.state3, self.state4]
        self.colour = (128, 0, 128)

class SShape(Shape):
    def __init__(self):
        Shape.__init__(self, 4, -2)
        self.state1 = [[0,1,1],
                       [1,1,0]]
        self.state2 = [[1,0],
                       [1,1],
                       [0,1]]
        self.states = [self.state1, self.state2]
        self.colour = (0, 255, 0)

class ZShape(Shape): # backward S
    def __init__(self):
        Shape.__init__(self, 4, -2)
        self.state1 = [[1,1,0],
                       [0,1,1]]
        self.state2 = [[0,1],
                       [1,1],
                       [1,0]]
        self.states = [self.state1, self.state2]
        self.colour = (255, 0, 0)

class LShape(Shape):
    def __init__(self):
        Shape.__init__(self, 4, -3)
        self.state1 = [[1,0],
                       [1,0],
                       [1,1]]
        self.state2 = [[0,0,1],
                       [1,1,1]]
        self.state3 = [[1,1],
                       [0,1],
                       [0,1]]
        self.state4 = [[1,1,1],
                       [1,0,0]]                       
        self.states = [self.state1, self.state2, self.state3, self.state4]
        self.colour = (0, 0, 255)

class JShape(Shape): # backward L
    def __init__(self):
        Shape.__init__(self, 4, -3)
        self.state1 = [[0,1],
                       [0,1],
                       [1,1]]
        self.state2 = [[1,1,1],
                       [0,0,1]]
        self.state3 = [[1,1],
                       [1,0],
                       [1,0]]
        self.state4 = [[1,0,0],
                       [1,1,1]]
        self.states = [self.state1, self.state2, self.state3, self.state4]
        self.colour = (255, 165, 0)

shapes = [OShape(), IShape(), TShape(), SShape(), ZShape(), LShape(), JShape()]

def get_shape():
    return random.choice(shapes)

def create_grid(filled_colours):
    m = GRID_WIDTH // BLOCK_SIZE
    n = GRID_HEIGHT // BLOCK_SIZE
    # initialize n x m grid with black blocks
    grid = [[(0,0,0) for _ in range(m)] for _ in range(n)]
    for i in range(n): # "y-value"
        for j in range(m): # "x-value"
            if (j,i) in filled_colours: # (x,y)
                grid[i][j] = filled_colours[(j,i)]
    return grid

def draw_grid(screen, grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # draw.rect: (left, top, width, height), thickness
            pygame.draw.rect(screen, grid[i][j], (X_GRID + j*BLOCK_SIZE, Y_GRID + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    # border
    pygame.draw.rect(screen, (255, 0, 0), (X_GRID, Y_GRID, GRID_WIDTH, GRID_HEIGHT), 5)

def draw_grid_lines(screen, grid):
    for i in range(len(grid)):
        # draw horizontal lines from starting x point
        pygame.draw.line(screen, (128,128,128), (X_GRID, Y_GRID + i*BLOCK_SIZE), \
            (X_GRID + GRID_WIDTH, Y_GRID + i*BLOCK_SIZE))
        for j in range(len(grid[i])+1):
            # draw vertical lines from starting y point
            pygame.draw.line(screen, (128, 128, 128), (X_GRID + j*BLOCK_SIZE, Y_GRID), \
                (X_GRID + j*BLOCK_SIZE, Y_GRID + GRID_HEIGHT))

def draw_text(screen, text, size, color, x, y):
    font = pygame.font.SysFont("century gothic", size, bold=True)
    text = font.render(text, 1, color)

    screen.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

def draw_screen(screen, grid, curr_score=0, prev_score=0):
    screen.fill((0, 0, 0))

    draw_text(screen, 'Tetris', 60, (255, 255, 255), X_GRID+GRID_WIDTH/2, 30)
    draw_grid(screen, grid)
    draw_grid_lines(screen, grid)

    # current score
    text = 'Score: ' + str(curr_score)
    # starting position for the text
    start_x = X_GRID + GRID_WIDTH + 100 # 50 to the right of grid
    start_y = Y_GRID + GRID_HEIGHT/2 + 150  
    draw_text(screen, text, 30, (255, 255, 255), start_x, start_y)

    # high score
    text = 'High Score: ' + str(prev_score)
    draw_text(screen, text, 30, (255, 255, 255), start_x, start_y+50) # 50 units below the previous line

def get_position(shape):
    # get position of blocks of current shape
    state = shape.states[shape.rotation % len(shape.states)]
    positions = [(j+shape.x, i+shape.y) for i in range(len(state)) for j in range(len(state[0])) if state[i][j] == 1]
    return positions

def is_valid_move(shape, grid):
    valid_positions = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == (0,0,0):
                valid_positions.append((j, i))

    positions = get_position(shape)

    for (x,y) in positions:
        # ignore pieces with negative y values (when a piece first starts)
        if (x,y) not in valid_positions and y >= 0: 
                return False
    return True

def clear_rows(grid, filled_colours):
    counter = 0
    shift_down = [0] * len(grid)
    for i in range(len(grid)-1, -1, -1): # start from bottom row
        if (0,0,0) not in grid[i]: # row is all filled
            counter += 1
            for k in range(i):
                shift_down[k] += 1  # number of times to shift row index k
            for j in range(len(grid[0])):
                del filled_colours[(j,i)]
    if counter:
        for (x,y) in sorted(filled_colours.keys(), key=lambda x:-x[1]): # sort from bottom row up
            # move original rows down shift_down[y] spots
            filled_colours[(x, y+shift_down[y])] = filled_colours.pop((x,y))
    return counter # for counting score

def draw_next_shape(screen, shape):
    # starting position for the text and shape
    start_x = X_GRID + GRID_WIDTH + 50 # 50 to the right of grid
    start_y = Y_GRID + GRID_HEIGHT/2 - 100  
    draw_text(screen, 'Next Shape', 30, (255, 255, 255), start_x+50, start_y-30)

    state = shape.states[0] # first rotation state
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j]:
                pygame.draw.rect(screen, shape.colour, (start_x + j*BLOCK_SIZE, start_y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

def check_if_game_end(positions):
    for (_,y) in positions:
        if y <= 0: # y=0 means you hit the top
            return True
    return False

def get_high_score():
    with open('high_score.txt', 'r') as f:
        score = f.readline().strip()
    return score

def write_score(new_score):
    score = get_high_score()
    with open('high_score.txt', 'w') as f:
        if int(score) > new_score:
            f.write(str(score))

def main_helper(screen):
    filled_colours = {} # {(x,y):(R,G,B)}
    current_piece = get_shape()
    current_piece.reset() # reset the initial position and rotation state
    next_piece = get_shape()
    get_next_piece = False

    curr_time = 0
    clock = pygame.time.Clock()
    
    curr_score = 0
    prev_score = get_high_score()

    run = True
    while run:
        grid = create_grid(filled_colours)

        fall_time = 0.4 # higher = fall slower
        curr_time += clock.get_rawtime() # in milliseconds
        clock.tick()

        if curr_time/1000 >= fall_time:
            curr_time = 0
            current_piece.y += 1
            # if you can't drop it down one unit (and the block is not at the top)
            if not (is_valid_move(current_piece, grid)):
                current_piece.y -= 1
                get_next_piece = True # the piece has settled, can get the next one

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(is_valid_move(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(is_valid_move(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(is_valid_move(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_SPACE:
                    current_piece.rotation += 1
                    if not(is_valid_move(current_piece, grid)):
                        current_piece.rotation -= 1

        positions = get_position(current_piece)

        for (x,y) in positions:
            if y >= 0: # don't draw when self.y is negative
                grid[y][x] = current_piece.colour

        if get_next_piece: # previous piece has reached the bottom
            for (x,y) in positions:
                filled_colours[(x,y)] = current_piece.colour
            current_piece = next_piece
            current_piece.reset()
            next_piece = get_shape()
            get_next_piece = False
            curr_score += clear_rows(grid, filled_colours) * 10

        draw_screen(screen, grid, curr_score, prev_score)
        draw_next_shape(screen, next_piece)
        pygame.display.flip()

        if check_if_game_end(filled_colours):
            screen.fill((0,0,0))
            draw_text(screen, "You have lost", 40, (255,255,255), WIDTH/2, HEIGHT/2)
            draw_text(screen, "Score: " + str(curr_score), 40, (255,255,255), WIDTH/2, HEIGHT/2+50)
            pygame.display.flip()
            pygame.time.delay(3000)
            write_score(curr_score)
            run = False
            
def main(screen):
    run = True
    while run:
        screen.fill((0,0,0))
        draw_text(screen, 'Press any key to start', 40, (255,255,255), \
            WIDTH/2, HEIGHT/2)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main_helper(screen)

    pygame.display.quit()

pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tetris')
main(screen)

