import pygame
pygame.init()

from neutreeko.constants import *
from neutreeko.game import Game

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Neutreeko')

END_FONT = pygame.font.Font('freesansbold.ttf', 32)

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def display_message(winner):
    pygame.draw.rect(WIN, GREEN, (SQUARE_SIZE, 1.5*SQUARE_SIZE, 3*SQUARE_SIZE, 2*SQUARE_SIZE))
    end_text = END_FONT.render("Player " + winner + " won!", 1, BLACK)
    WIN.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
                game.update()
                winner = game.checkWin()
                if (winner > 0): 
                    display_message(str(winner))
                    run = False

        game.update()
        pygame.display.update()

    pygame.quit()


main()