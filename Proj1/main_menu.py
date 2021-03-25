import pygame
import pygame_menu
from neutreeko.constants import *
from neutreeko.game import Game
from minimax.algorithm import *

pygame.init()

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Neutreeko')
END_FONT = pygame.font.Font('freesansbold.ttf', 32)
global global_mode
global_mode = "pvp"

def get_row_col_from_mouse(pos):
    x, y = pos
    x -= 200
    y -= 220
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def display_message(winner):
    pygame.draw.rect(WIN, GREEN, (SQUARE_SIZE, 1.5*SQUARE_SIZE, 3*SQUARE_SIZE, 2*SQUARE_SIZE))
    end_text = END_FONT.render("Player " + winner + " won!", 1, BLACK)
    WIN.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)

def drawCards():
    #WIN.fill(PURPLE)
    pygame.draw.rect(WIN, GREY, (150, 100, 500, 100))
    pygame.draw.rect(WIN, GREY, (150, 650, 500, 100))
    pygame.draw.rect(WIN, WHITE, (620, 160, 25, 200)) #Barra branca
    pygame.draw.rect(WIN, BLUE, (620, 360, 25, 200)) #Barra preta

def start():
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
                value, new_board = minimax(game.board, 6, 2, float('-inf'), float('+inf'))
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


def start_the_game():
    start()

def set_mode(value, mode):
    global global_mode
    menu.remove_widget(quit)

    if mode == 1 and global_mode == "pvc":
        global_mode = "pvp"
        menu.remove_widget(select_method)
        menu.remove_widget(select_heuristic) 

    elif mode == 1 and global_mode == "cvc":
        global_mode = "pvp"
        menu.remove_widget(select_difficulty_pc1)
        menu.remove_widget(select_difficulty_pc2) 

    elif mode == 2 and global_mode == "pvp":
        global_mode = "pvc"
        menu.add_generic_widget(select_method)
        menu.add_generic_widget(select_heuristic)
    elif mode == 2 and global_mode == "cvc":
        global_mode = "pvc"
        menu.remove_widget(select_difficulty_pc1)
        menu.remove_widget(select_difficulty_pc2)
        menu.add_generic_widget(select_method)
        menu.add_generic_widget(select_heuristic)

    elif mode == 3 and global_mode == "pvp":
        global_mode = "cvc"
        menu.add_generic_widget(select_difficulty_pc1)
        menu.add_generic_widget(select_difficulty_pc2)
    elif mode == 3 and global_mode == "pvc":
        global_mode = "cvc"
        menu.remove_widget(select_method)
        menu.remove_widget(select_heuristic) 
        menu.add_generic_widget(select_difficulty_pc1)
        menu.add_generic_widget(select_difficulty_pc2)

    menu.add_generic_widget(quit) 
    
    

def set_method(value, method):
    #To Do
    pass

def set_heuristic(value, heuristic):
    #To Do
    pass

def set_difficulty_pc1(value, difficulty):
    #To Do
    pass

def set_difficulty_pc2(value, difficulty):
    #To Do
    pass

mytheme = pygame_menu.themes.THEME_DARK.copy()

myimage = pygame_menu.baseimage.BaseImage(image_path='src/back.jpg', drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
mytheme.background_color = myimage
mytheme.widget_font_color = (255,255,255)
mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE
mytheme.title_background_color = (1,99,110,255)
mytheme.widget_font_size = 30
mytheme.widget_margin = (0,20)
menu = pygame_menu.Menu(WIDTH, HEIGHT, 'Neutreeko', theme=mytheme)

menu.add.button('Play', start_the_game)
menu.add.selector('Mode :', [('Player v Player', 1), ('Player v AI', 2), ('AI v AI', 3)], onchange=set_mode)
select_method = menu.add.selector('Search Method :', [('Minimax', 1), ('Minimax com Alpha-Beta Pruning', 2)], onchange=set_method)
select_heuristic = menu.add.selector('Heuristic :', [('Simple', 1), ('Advanced', 2), ('Complex', 3)], onchange=set_heuristic)
select_difficulty_pc1 = menu.add.selector('Pc1 difficulty :', [('Simple', 1), ('Advanced', 2), ('Complex', 3)], onchange=set_difficulty_pc1)
select_difficulty_pc2 = menu.add.selector('Pc2 difficulty :', [('Simple', 1), ('Advanced', 2), ('Complex', 3)], onchange=set_difficulty_pc2)
quit = menu.add.button('Quit', pygame_menu.events.EXIT)
menu.remove_widget(select_method)
menu.remove_widget(select_heuristic)
menu.remove_widget(select_difficulty_pc1)
menu.remove_widget(select_difficulty_pc2)




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