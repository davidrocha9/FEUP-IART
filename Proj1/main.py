import pygame
pygame.init()
 
from neutreeko.constants import *
from neutreeko.game import Game
from minimax.algorithm import minimax

FPS = 60

WIN = pygame.display.set_mode((720, 720))
pygame.display.set_caption('Neutreeko')

END_FONT = pygame.font.Font('freesansbold.ttf', 32)

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE - 2
    col = x // SQUARE_SIZE - 2
    return row, col

def display_message(winner):
    pygame.draw.rect(WIN, PURPLE, (SQUARE_SIZE, 1.5*SQUARE_SIZE, 3*SQUARE_SIZE, 2*SQUARE_SIZE))
    end_text = END_FONT.render("Player " + winner + " won!", 1, BLACK)
    WIN.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)

def drawCards():
    WIN.fill(PURPLE)
    pygame.draw.rect(WIN, GREY, (110, 30, 500, 100))
    pygame.draw.rect(WIN, GREY, (110, 590, 500, 100))
    pygame.draw.rect(WIN, WHITE, (620, 160, 25, 200)) #Barra branca
    pygame.draw.rect(WIN, BLUE, (620, 360, 25, 200)) #Barra preta

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    whiteBarY = 160
    blackBarY = 360
    drawCards()

    while run:
        clock.tick(FPS)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if game.turn == 2:
                value, new_board = minimax(game.board, 5, 2, float('-inf'), float('+inf'))
                game.board = new_board
                game.update()
                winner = game.board.checkWin()
                if (winner > 0): 
                    display_message(str(winner)) 
                    run = False
                game.turn = 1
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)

                    game.update()
                    winner = game.board.checkWin()
                    if (winner > 0): 
                        display_message(str(winner)) 
                        run = False

        game.update()
        pygame.display.update()
        

    pygame.quit()


main()