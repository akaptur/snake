from pygame.locals import *
import pygame
import pdb
import sys
import random
SCREEN = pygame.display.set_mode((400,400))
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,200,0)
RED = (255,0,0)

class SnakeGame():

    def __init__(self):
        """ Initializes 20x20 board. Each square has state (food, snake, empty).""" 
        self.board = [['Empty' for i in range(20)] for j in range(20)]
        self.snake_coords = [[10,10],[10,9],[10,8]]
        self.snake_momentum = 'right'


    def start_game(self):
        self.new_food()
        self.place_snake() 


    def new_food(self):
        newfood = [random.randint(0,19),random.randint(0,19)]
        if self.board[newfood[0]][newfood[1]] != 'Empty': #check if square occupied by food or snake
            self.new_food()
        else: 
            self.board[newfood[0]][newfood[1]] = 'Food'


    def place_snake(self):
        for segment in self.snake_coords:
            snake_row, snake_col = segment #unpack list of coordinates
            self.board[snake_row][snake_col] = 'Snake'


    def draw_board(self):
        SCREEN.fill(WHITE)
        pygame.draw.rect(SCREEN, BLUE, (0,380,20,20))
        for col in range(20):
            for row in range(20):
                state = self.board[row][col]
                if state == 'Snake':
                    pygame.draw.rect(SCREEN, GREEN, (col*20,row*20,20,20))
                    pygame.draw.rect(SCREEN, BLACK, (col*20,row*20,20,20),2)
                elif state == 'Food':
                    pygame.draw.rect(SCREEN, BLUE, (col*20 + 5, row*20 + 5, 10, 10))


    def snake_advance(self):
        game_is_over = False
        """ This function moves the snake ahead by one square in the direction of its momentum."""
        snake_row, snake_col = self.snake_coords[0] #first element of snake_coords is the head
        momentum = self.snake_momentum
        if momentum == 'up':
            new_square_row, new_square_col = snake_row - 1, snake_col
        elif momentum == 'down':
            new_square_row, new_square_col = snake_row + 1, snake_col
        elif momentum == 'left':
            new_square_row, new_square_col = snake_row, snake_col - 1 
        elif momentum == 'right':
            new_square_row, new_square_col = snake_row, snake_col + 1
        #implement wrapping
        if new_square_row == 20:
            new_square_row = 0
        if new_square_row == -1:
            new_square_row = 19
        if new_square_col == 20:
            new_square_col = 0
        if new_square_col == -1:
            new_square_col = 19
        #if snake wraps on itself, game over
        if [new_square_row, new_square_col] in self.snake_coords:
            game_is_over = True
        self.snake_coords.insert(0,[new_square_row, new_square_col])
        tail_row, tail_col = self.snake_coords.pop() #remove trailing square unless snake ate food
        if self.board[new_square_row][new_square_col] == 'Food':
            self.snake_coords.append([tail_row, tail_col])
            self.new_food()
        self.board[tail_row][tail_col] = 'Empty'
        self.place_snake()

        return game_is_over

    def game_over(self):
        losing_text1 = ' You lose!                ____'
        losing_text2 = ' ________________________/ x  \___/'
        losing_text3 = '<_/_\_/_\_/_\_/_\_/_\_/_______/   \ '

        pygame.font.init()
        myfont = pygame.font.SysFont('courier', 14, bold=1)
        pygame.draw.rect(SCREEN, RED, (30,30,300,80))
        label1 = myfont.render(losing_text1, 1, BLACK)
        label2 = myfont.render(losing_text2, 1, BLACK)
        label3 = myfont.render(losing_text3, 1, BLACK)
        SCREEN.blit(label1, (40,50))
        SCREEN.blit(label2, (40,65))
        SCREEN.blit(label3, (40,80))

    def keystroke(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.snake_momentum = 'down'
            elif event.key == pygame.K_RIGHT:
                self.snake_momentum = 'right'
            elif event.key == pygame.K_LEFT:
                self.snake_momentum = 'left'
            elif event.key == pygame.K_UP:
                self.snake_momentum = 'up'

    def print_state(self):
        """ This function is a debugging tool."""
        for row in range(20):
            for col in range(19):
                print self.board[row][col][0], #commas suppress line breaks
            print self.board[row][19][0]
        print '\n'
        print self.snake_coords[0]


    def accelerate(self, frame_step):
        return int(frame_step*.9)

s = SnakeGame()
s.start_game()

# s.print_momentum()

frames = 0 
frame_step = 35
acceler_step = 600
game_over = False

while not game_over:
    frames += 1
    if frames % frame_step == 0:
        game_over = s.snake_advance()
    if frames % acceler_step == 0:
        frame_step = s.accelerate(frame_step)
    for event in pygame.event.get():
        s.keystroke(event)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    s.draw_board()
    pygame.display.update()

#when while loop exits, game is over

s.game_over()
while game_over: #continue to display game over screen until the user exits
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()



