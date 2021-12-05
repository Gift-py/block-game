import pygame
import random

pygame.init()
sw = 800
sh = 800
ROWS = 50

GREY = (128, 128, 128)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

win = pygame.display.set_mode((sw, sw))
pygame.display.set_caption('Brick Breaker')
#font = pygame.font.SysFont('comicsans', 50)

#for frame rate
clock = pygame.time.Clock()
gameover = False


class Paddle(object):
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.xx = self.x + self.w
        self.yy = self.y + self.h

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))
  
class Ball(object):
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.vx = random.choice([-2, -1, 0, 1, 2])
        self.vy = random.randint(2, 3)
        self.xx = self.x + self.w
        self.yy = self.y + self.h

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))

    def move(self):
        self.x += self.vx
        self.y += self.vy

class Blocks(object):
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.color = BLACK

    def reset(self):
        self.color = BLACK

    def is_block(self):
        return self.color == RED

    def is_brick(self):
        return self.color == GREEN

    def make_block(self):
        self.color = RED

    def make_brick(self):
        self.color = GREEN

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


player =  Paddle(sw/2-25, sh-100, 100, 5, WHITE)
ball = Ball(sw/2-2.5, sh-250, 5, 5, WHITE)

def make_grid(rows, width):
    grid = []
    gap = width//rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            block = Blocks(i, j, gap, rows)
            grid[i].append(block)
    return grid

def draw_grid(win, rows, width):
    gap = width//rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))

def draw(win, grid, rows, width):
    for row in grid:
        for block in row:
            block.draw(win)
    player.draw(win)
    ball.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap

    return row, col

def paddle_move():
    if pygame.mouse.get_pos()[0] - player.w//2 < 0:
        player.x = 0
    if pygame.mouse.get_pos()[0] + player.w//2 > sw:
        player.x = sw - player.w
    else:
        player.x = pygame.mouse.get_pos()[0] - player.w//2

def ball_collisions(): 
#with paddle and edges of win
    angle = 0
    if (ball.x >= player.x and ball.x <= player.x+player.w) or (ball.x+ball.w >= player.x and ball.x+ball.w <= player.x+player.w):
        if ball.y+ball.h >= player.y and ball.y+ball.h <= player.y+ball.h:    
            ball.vy *= -1

    #for edges of the screen
    if ball.x + ball.w >= sw:
        ball.vx *= -1
    if ball.x + ball.w <= 0:
        ball.vx *= -1
    if ball.y <= 0:
        ball.vy *= -1

bricks = []
blocks = []

def brick_coll():
    for brick in bricks:
        if (ball.x >= brick.x and ball.x <= (sw//ROWS)+brick.x) or (ball.x+ball.w >= brick.x and ball.x+ball.w <= (sw//ROWS)+brick.x):
            if(ball.y >= brick.y and ball.y <= (sw//ROWS)+brick.y) or (ball.y+ball.h >= brick.y and ball.y <= (sw//ROWS)+brick.y):            
                if brick.is_brick():
                    brick.reset()
                    bricks.pop(bricks.index(brick))
                    ball.vy *= -1
        
        if (ball.y >= brick.y and ball.y <= (sw//ROWS)+brick.y) or (ball.y+ball.h >= brick.y and ball.y+ball.h <= (sw//ROWS)+brick.y):
            if (ball.x >= brick.x and ball.x <= (sw//ROWS)+brick.x) or (ball.x+ball.w >= brick.x and ball.x+ball.w <= (sw//ROWS)+brick.x):
                brick.reset()
                bricks.pop(bricks.index(brick))
                ball.vx *= -1
                ball.vy *= -1

def block_coll():
    for block in blocks:
        if (ball.x >= block.x and ball.x <= (sw//ROWS)+block.x) or (ball.x+ball.w >= block.x and ball.x+ball.w <= (sw//ROWS)+block.x):
            if(ball.y >= block.y and ball.y <= (sw//ROWS)+block.y) or (ball.y+ball.h >= block.y and ball.y <= (sw//ROWS)+block.y): 
                ball.vy *= -1

        if (ball.y >= block.y and ball.y <= (sw//ROWS)+block.y) or (ball.y+ball.h >= block.y and ball.y+ball.h <= (sw//ROWS)+block.y):
            if (ball.x >= block.x and ball.x <= (sw//ROWS)+block.x) or (ball.x+ball.w >= block.x and ball.x+ball.w <= (sw//ROWS)+block.x):
                ball.vx *= -1
                ball.vy *= -1

def main(win, width):
    grid = make_grid(ROWS, width)
    key = pygame.key.get_pressed()
    run = True

    while run:            
        draw(win, grid, ROWS, width)
        clock.tick(100)
        if not gameover:
            paddle_move()
            ball_collisions()
            ball.move()
            brick_coll()
            block_coll()
        
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, ROWS, width)
            block = grid[row][col]
            print(block, row, col, 'aii')
            brick = block
            bricks.append(brick)
            brick.make_brick()

        if pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, ROWS, width)
            block = grid[row][col]
            print(block, row, col, 'oii')
            bloc = block
            blocks.append(bloc)
            bloc.make_block()

        if key[pygame.K_BACKSPACE]:
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos, ROWS, width)
            block = grid[row][col]
            bloc = block
            if bloc.is_brick():
                bricks.pop(bricks.index(bloc))
                bloc.reset()
            if bloc.is_block():
                blocks.pop(blocks.index(bloc))
                bloc.reset
        
        
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()

main(win, sw)


#if i click run ball should not move
