import pygame
from pygame import gfxdraw
import pygame_menu
import time
from neutreeko.constants import *
from neutreeko.game import Game
from minimax.algorithm import AI
import time
import random

pygame.init()

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Neutreeko')
END_FONT = pygame.font.Font('freesansbold.ttf', 32)
talkFont = pygame.font.Font('freesansbold.ttf', 15)
global global_mode, global_heuristic, global_method, global_pc1, global_pc2
global_mode = "pvp"
global_heuristic = 2
global_method = 1
global_pc1 = 1
global_pc2 = 1

lines = ["This is all theory.", "*looks at ceiling and scratches head*", "Takes, takes and takes... I think this is winning.", "Is this a move? Probably. Let's play it.", "Let's keep going.", "Chat, this has to be winning!", "I'll just play my juicer here.", "If takes I just take, and then I must be winning.", "I go here, here, here and here and I win."]

def get_row_col_from_mouse(pos):
    x, y = pos
    x -= 175
    y -= 220
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def display_message(winner):
    pygame.draw.rect(WIN, (1,99,110,255), (150, 250, 500, 300))
    end_text = END_FONT.render("Player " + winner + " won!", 1, BLACK)
    WIN.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    time.sleep(3)

def drawCards():
    #WIN.fill(PURPLE)
    pygame.draw.rect(WIN, CARDCOLOR, (150, 90, 500, 100), width=0, border_radius=10, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)
    pygame.draw.rect(WIN, WHITE, (680, 220, 25, 225)) #Barra branca
    pygame.draw.rect(WIN, BLUE, (680, 445, 25, 225)) #Barra preta

def updateBars(p1, p2):
    total = p1 + p2
    p1Percentage = float(p1/total)
    p2Percentage = float(p2/total)
    pygame.draw.rect(WIN, WHITE, (680, 220, 25, p2Percentage * 450)) #Barra branca
    pygame.draw.rect(WIN, BLUE, (680, 220 + p2Percentage * 450, 25, p1Percentage * 450)) #Barra preta

def drawWelcome():
    pygame.draw.rect(WIN, WHITE, (160, 100, 350, 80), width=0, border_radius=10, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)
    pygame.gfxdraw.filled_polygon(WIN, [[500, 115], [500, 160], [550, 138]], WHITE)
    hint = talkFont.render("Let's see what you have prepared for me.", True, (0,0,0))
    WIN.blit(hint, (175, 130))

def drawLine():
    pygame.draw.rect(WIN, WHITE, (160, 100, 350, 80), width=0, border_radius=10, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)
    pygame.gfxdraw.filled_polygon(WIN, [[500, 115], [500, 160], [550, 138]], WHITE)
    x = random.randint(0,len(lines)-1)
    hint = talkFont.render(lines[x], True, (0,0,0))
    WIN.blit(hint, (175, 130))

def drawEnding(player):
    pygame.draw.rect(WIN, WHITE, (160, 100, 350, 80), width=0, border_radius=10, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)
    pygame.gfxdraw.filled_polygon(WIN, [[500, 115], [500, 160], [550, 138]], WHITE)
    if (player == 2):
        hint = talkFont.render("Good, but not good enough for Magnus.", True, (0,0,0))
    else:
        hint = talkFont.render("How did I not see that? I'm so bad.", True, (0,0,0))
    WIN.blit(hint, (175, 130))

def start():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    ai = AI()
    whiteBarY = 160
    blackBarY = 360
    drawCards()
    hint = END_FONT.render('Press H for a Hint', True, (0,0,0))
    WIN.blit(hint, (265, 700))
    image = pygame.image.load(r'.\assets\hikaru.png')
    WIN.blit(image, (550, 100))
    drawWelcome()
    
    while run:
        clock.tick(FPS)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif global_mode == "pvp":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    movePlayed = game.select(row, col)
                    if (movePlayed == 1):
                        eval1 = game.board.evaluationPlayer(1)
                        eval2 = game.board.evaluationPlayer(2)
                        updateBars(eval1, eval2)
                    game.update()
                    winner = game.board.checkWin()
                    if (winner > 0): 
                        display_message(str(winner)) 
                        time.sleep(1)
                        run = False
            elif global_mode == "pvc":
                print(global_method)
                if global_method == 1:
                    if game.turn == 2:
                        value, new_board, res = ai.minimax(game.board, global_heuristic, 2, float('-inf'), float('+inf'), 0)
                        eval1 = new_board.evaluationPlayer(1)
                        eval2 = new_board.evaluationPlayer(2)
                        updateBars(eval1, eval2)
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
                            movePlayed = game.select(row, col)
                            if (movePlayed == 1):
                                eval1 = game.board.evaluationPlayer(1)
                                eval2 = game.board.evaluationPlayer(2)
                                updateBars(eval1, eval2)
                            game.update()
                            winner = game.board.checkWin()
                            if (winner > 0): 
                                display_message(str(winner)) 
                                run = False
                elif global_method == 2:
                    if game.turn == 2:
                        value, new_board, res = ai.minimax_ab(game.board, global_heuristic, 2, float('-inf'), float('+inf'), 0)
                        eval1 = new_board.evaluationPlayer(1)
                        eval2 = new_board.evaluationPlayer(2)
                        updateBars(eval1, eval2)
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
                            movePlayed = game.select(row, col)
                            if (movePlayed == 1):
                                eval1 = game.board.evaluationPlayer(1)
                                eval2 = game.board.evaluationPlayer(2)
                                updateBars(eval1, eval2)
                            game.update()
                            winner = game.board.checkWin()
                            if (winner > 0): 
                                display_message(str(winner)) 
                                run = False
            elif global_mode == "cvc":
                if game.turn == 1:
                    value, new_board, res = ai.minimax_ab(game.board, global_pc2, 1, float('-inf'), float('+inf'), 0)
                    time.sleep(1)
                    eval1 = new_board.evaluationPlayer(1)
                    eval2 = new_board.evaluationPlayer(2)
                    updateBars(eval1, eval2)
                    game.board = new_board
                    game.update()
                    winner = game.board.checkWin()
                    if (winner > 0): 
                        time.sleep(1)
                        display_message(str(winner)) 
                        run = False
                    game.turn = 2
                elif game.turn == 2:
                    value, new_board, res = ai.minimax_ab(game.board, global_pc1, 2, float('-inf'), float('+inf'), 0)
                    time.sleep(1)
                    eval1 = new_board.evaluationPlayer(1)
                    eval2 = new_board.evaluationPlayer(2)
                    updateBars(eval1, eval2)
                    game.board = new_board
                    game.update()
                    winner = game.board.checkWin()
                    if (winner > 0): 
                        time.sleep(1)
                        display_message(str(winner)) 
                        run = False
                    game.turn = 1

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
    global global_method
    if method == 1: global_method = 1
    elif method == 2: global_method = 2

def set_heuristic(value, heuristic):
    global global_heuristic
    if heuristic == 1: global_heuristic = 2
    elif heuristic == 2: global_heuristic = 4
    elif heuristic == 3: global_heuristic = 6
    

def set_difficulty_pc1(value, difficulty1):
    global global_pc1
    if difficulty1 == 1: global_pc1 = 2
    elif difficulty1 == 2: global_pc1 = 3
    elif difficulty1 == 3: global_pc1 = 4

def set_difficulty_pc2(value, difficult2):
    global global_pc2
    if difficulty2 == 1: global_pc2 = 2
    elif difficulty2 == 2: global_pc2 = 3
    elif difficulty2 == 3: global_pc2 = 4

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