import pygame

pygame.init()
from bots.botmethods import *

# Game Loop
def start():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    ai = AI()
    botStarted = False
    drawBars(WIN)

    while run:
        clock.tick(FPS)
        pygame.display.update()

        # If a player asks for a hint it doesn't need pygame events
        if game.pressedHint is True:
            if game.turn == 1:
                game.p1HintCounter += 1
            elif againstPc is False:
                game.p2HintCounter += 1
            game.pressedHint = False
            drawHintBoard(game, againstPc)
            game.update()
            pygame.display.update()
            if againstPc is False or (againstPc is True and game.turn != 2):
                calculateHint(game, ai, WIN, againstPc)
        # CvC handler
        elif global_mode == "cvc":
            game.update()
            pygame.display.update()
            if computerplay(game, ai, global_pc1, global_pc2, global_evaluation) == 1:
                game.update()
                pygame.display.update()
                run = False
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif global_mode == "pvp":
                    image = pygame.image.load(r'.\assets\defaultplayer.png')
                    player1 = nameFont.render(global_name1[0], True, (0, 0, 0))
                    player2 = nameFont.render(global_name2[0], True, (0, 0, 0))
                    drawHintBoard(game, againstPc)
                    WIN.blit(player2, (270, 160))
                    WIN.blit(player1, (270, 740))
                    WIN.blit(image, (180, 100))
                    WIN.blit(image, (180, 680))
                    if event.type == pygame.KEYDOWN:
                        if event.unicode == 'h':
                            game.pressedHint = True
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        row, col = get_row_col_from_mouse(pos)
                        movePlayed = game.select(row, col)
                        if movePlayed == 1:
                            eval1 = game.board.evaluationPlayer(1)
                            eval2 = game.board.evaluationPlayer(2)
                            updateBars(WIN, eval1, eval2)
                            game.update()
                            winner = game.board.checkWinAndTie()
                            if winner >= 0:
                                display_message(WIN, str(winner))
                                time.sleep(1)
                                run = False
                # PvC handler
                elif global_mode == "pvc":
                    image = pygame.image.load(r'.\assets\lamp.png')
                    image1 = pygame.image.load(r'.\assets\defaultplayer.png')
                    player1 = nameFont.render(global_name1[0], True, (0, 0, 0))
                    WIN.blit(player1, (270, 730))
                    WIN.blit(image1, (180, 670))
                    WIN.blit(image, (20, 350))
                    drawHintBoard(game, againstPc)
                    if botStarted is False:
                        drawCards(WIN)
                        drawWelcome(WIN, global_heuristic)
                        drawName(WIN, global_heuristic)
                        botStarted = True
                        if global_heuristic == 2:
                            global_name2[0] = "XQC"
                            image = pygame.image.load(r'.\assets\xqc.png')
                            WIN.blit(image, (550, 100))
                        elif global_heuristic == 4:
                            global_name2[0] = "Andrea"
                            image = pygame.image.load(r'.\assets\botez.png')
                            WIN.blit(image, (550, 100))
                        elif global_heuristic == 5:
                            global_name2[0] = "Hikaru"
                            image = pygame.image.load(r'.\assets\hikaru.png')
                            WIN.blit(image, (550, 100))
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN or game.turn == 2 and game.pressedHint is False:
                        if global_method == 1:
                            if method_1(game, ai, event, global_heuristic, global_evaluation) == 1:
                                run = False
                        elif global_method == 2:
                            if method_2(game, ai, event, global_heuristic, global_evaluation) == 1:
                                run = False
        game.update()
        pygame.display.update()


def start_the_game():
    image = pygame.image.load(r'.\assets\back.jpg')
    WIN.blit(image, (0, 0))
    if global_mode == "pvp":
        againstPc = False
    elif global_mode == "pvc":
        againstPc = True
    start()

# Functions related to the Menu
def set_mode(value, mode):
    global global_mode
    menu.remove_widget(quit)

    if mode == 1 and global_mode == "pvc":
        global_mode = "pvp"
        menu.remove_widget(nome1)
        menu.remove_widget(select_method)
        menu.remove_widget(select_heuristic)
        menu.remove_widget(select_evaluation)
        menu.add_generic_widget(nome1)
        menu.add_generic_widget(nome2)

    elif mode == 1 and global_mode == "cvc":
        global_mode = "pvp"
        menu.remove_widget(select_method_pc1)
        menu.remove_widget(select_method_pc2)
        menu.remove_widget(select_difficulty_pc1)
        menu.remove_widget(select_difficulty_pc2)
        menu.add_generic_widget(nome1)
        menu.add_generic_widget(nome2)

    elif mode == 2 and global_mode == "pvp":
        global_mode = "pvc"
        menu.remove_widget(nome1)
        menu.remove_widget(nome2)
        menu.add_generic_widget(nome1)
        menu.add_generic_widget(select_method)
        menu.add_generic_widget(select_heuristic)
        menu.add_generic_widget(select_evaluation)

    elif mode == 2 and global_mode == "cvc":
        global_mode = "pvc"
        menu.remove_widget(select_method_pc1)
        menu.remove_widget(select_method_pc2)
        menu.remove_widget(select_difficulty_pc1)
        menu.remove_widget(select_difficulty_pc2)
        menu.add_generic_widget(nome1)
        menu.add_generic_widget(select_method)
        menu.add_generic_widget(select_heuristic)
        menu.add_generic_widget(select_evaluation)

    elif mode == 3 and global_mode == "pvp":
        global_mode = "cvc"
        menu.remove_widget(nome1)
        menu.remove_widget(nome2)
        menu.add_generic_widget(select_method_pc1)
        menu.add_generic_widget(select_method_pc2)
        menu.add_generic_widget(select_difficulty_pc1)
        menu.add_generic_widget(select_difficulty_pc2)
    elif mode == 3 and global_mode == "pvc":
        global_mode = "cvc"
        menu.remove_widget(nome1)
        menu.remove_widget(select_method)
        menu.remove_widget(select_heuristic)
        menu.remove_widget(select_evaluation)
        menu.add_generic_widget(select_method_pc1)
        menu.add_generic_widget(select_method_pc2)
        menu.add_generic_widget(select_difficulty_pc1)
        menu.add_generic_widget(select_difficulty_pc2)

    menu.add_generic_widget(quit)


def set_name1(name1):
    global global_name1
    global_name1[0] = name1


def set_name2(name2):
    global global_name2
    global_name2[0] = name2


def set_method(value, method):
    global global_method
    if method == 1:
        global_method = 1
    elif method == 2:
        global_method = 2
    elif method == 3:
        global_method = 3


def set_heuristic(value, heuristic):
    global global_heuristic
    if heuristic == 1:
        global_heuristic = 2
    elif heuristic == 2:
        global_heuristic = 4
    elif heuristic == 3:
        global_heuristic = 5

def set_evaluation(value, evaluation):
    global global_evaluation
    if evaluation == 1:
        global_evaluation = 1
    elif evaluation == 2:
        global_evaluation = 2


def set_difficulty_pc1(value, difficulty1):
    global global_pc1
    if difficulty1 == 1:
        global_pc1 = 2
    elif difficulty1 == 2:
        global_pc1 = 3
    elif difficulty1 == 3:
        global_pc1 = 5


def set_difficulty_pc2(value, difficulty2):
    global global_pc2
    if difficulty2 == 1:
        global_pc2 = 2
    elif difficulty2 == 2:
        global_pc2 = 3
    elif difficulty2 == 3:
        global_pc2 = 5

def set_method_pc1(value, method1):
    global global_method1
    if method1 == 1: global_method1 = 1
    if method1 == 2: global_method1 ==2

def set_method_pc2(value, method2):
    global global_method2
    if method2 == 1: global_method2 = 1
    if method2 == 2: global_method2 ==2


mytheme = pygame_menu.themes.THEME_DARK.copy()

myimage = pygame_menu.baseimage.BaseImage(image_path='assets/back.jpg',
                                          drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
mytheme.background_color = myimage
mytheme.widget_font_color = (255, 255, 255)
mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE
mytheme.title_background_color = (1, 99, 110, 255)
mytheme.widget_font_size = 30
mytheme.widget_margin = (0, 20)
menu = pygame_menu.Menu(WIDTH, HEIGHT, 'Neutreeko', theme=mytheme)

menu.add.button('Play', start_the_game)
menu.add.selector('Mode: ', [('Player v Player', 1), ('Player v AI', 2), ('AI v AI', 3)], onchange=set_mode)
nome1 = menu.add.text_input('Player1: ', default='Default', onchange=(set_name1))
nome2 = menu.add.text_input('Player2: ', default='Default', onchange=(set_name2))
select_method = menu.add.selector('Search Method: ',
                                  [('Minimax', 1), ('Minimax com Alpha-Beta Pruning', 2)],
                                  onchange=set_method)
select_heuristic = menu.add.selector('Heuristic: ', [('Simple', 1), ('Advanced', 2), ('Complex', 3)],
                                     onchange=set_heuristic)
select_evaluation = menu.add.selector('Evaluation Function: ', [('Simple', 1), ('Complex', 2)],
                                      onchange=set_evaluation)
select_method_pc1 = menu.add.selector('Pc1 method: ', [('Minimax', 1), ('Minimax com Alpha-Beta Pruning', 2)], onchange=set_method_pc1)
select_method_pc2 = menu.add.selector('Pc2 method: ', [('Minimax', 1), ('Minimax com Alpha-Beta Pruning', 2)], onchange=set_method_pc2)
select_difficulty_pc1 = menu.add.selector('Pc1 difficulty: ', [('Simple', 1), ('Advanced', 2), ('Complex', 3)],
                                          onchange=set_difficulty_pc1)
select_difficulty_pc2 = menu.add.selector('Pc2 difficulty: ', [('Simple', 1), ('Advanced', 2), ('Complex', 3)],
                                          onchange=set_difficulty_pc2)
quit = menu.add.button('Quit', pygame_menu.events.EXIT)
menu.remove_widget(select_method)
menu.remove_widget(select_heuristic)
menu.remove_widget(select_evaluation)
menu.remove_widget(select_method_pc1)
menu.remove_widget(select_method_pc2)
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
