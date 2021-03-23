import pygame
import pygame_menu
from neutreeko.constants import *
from neutreeko.game import Game

pygame.init()

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

def start():
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



def set_difficulty(value, difficulty):
    # To Do
    pass

def start_the_game():
    start()

def set_mode(value, mode):
    #To Do
    pass

def set_method(value, method):
    #To Do
    pass

def set_heuristic(value, heuristic):
    #To Do
    pass

menu = pygame_menu.Menu(WIDTH, HEIGHT, 'Neutreeko',
                       theme=pygame_menu.themes.THEME_DARK)

#menu.add.text_input('Name :', default='John Doe')
menu.add.button('Play', start_the_game)
menu.add.selector('Mode :', [('Player v Player', 1), ('Player v AI', 2), ('AI v AI', 3)], onchange=set_mode)
menu.add.selector('Search Method :', [('Minimax', 1), ('Minimax com Alpha-Beta Pruning', 2), ('Negamax', 3)], onchange=set_method)
menu.add.selector('Heuristic :', [('Simple', 1), ('Advanced', 2), ('Complex', 3)], onchange=set_heuristic)
#menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Quit', pygame_menu.events.EXIT)

def main():
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        if menu.is_enabled():
            menu.update(events)
            menu.draw(WIN)

        pygame.display.update()
    pygame.quit()

main()