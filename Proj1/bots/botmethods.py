from neutreeko.move import Move
from neutreeko.piece import Piece
from utils import *
import time


# Without cuts
def method_1(game, ai, event, diff, eval):
    # Bot Turn
    if game.turn == 2:
        tic = time.perf_counter()
        ai.counter = 0
        value, new_board = ai.minimax(game.board, diff, 2, float('-inf'), float('+inf'), eval)
        toc = time.perf_counter()
        print_stats((round((toc-tic),4)),ai.counter)
        game.turn = 1
        # Updating Visual Aspects
        eval1 = new_board.evaluationPlayer(1)
        eval2 = new_board.evaluationPlayer(2)
        updateBars(WIN, eval1, eval2)
        game.board = new_board
        game.update()
        winner = game.board.checkWinAndTie()
        # Checking if the game has ended
        if winner >= 0:
            drawEnding(winner, diff, WIN)
            display_message(WIN, str(winner))
            return 1
        drawLine(WIN, diff)
    # Player Turn
    else:
        # Hint
        if event.type == pygame.KEYDOWN:
            if event.unicode == 'h':
                game.pressedHint = True
        # Selecting piece/square
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
                    drawEnding(winner, diff, WIN)
                    display_message(WIN, str(winner))
                    return 1


# With Cuts
def method_2(game, ai, event, diff, eval):
    # Bot Turn
    if game.turn == 2:
        tic = time.perf_counter()
        ai.counter = 0
        value, new_board = ai.minimax_ab(game.board, diff, 2, float('-inf'), float('+inf'), eval)
        toc = time.perf_counter()
        print_stats((round((toc-tic),4)),ai.counter)
        game.turn = 1
        # Updating Visual Aspects
        eval1 = new_board.evaluationPlayer(1)
        eval2 = new_board.evaluationPlayer(2)
        updateBars(WIN, eval1, eval2)
        game.board = new_board
        game.update()
        winner = game.board.checkWinAndTie()
        # Checking if the game has ended
        if winner >= 0:
            drawEnding(winner, diff, WIN)
            display_message(WIN, str(winner))
            return 1
        drawLine(WIN, diff)
    # Player Turn
    else:
        # Hint
        if event.type == pygame.KEYDOWN:
            if event.unicode == 'h':
                game.pressedHint = True
        # Selecting piece/square
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
                    drawEnding(winner, diff, WIN)
                    display_message(WIN, str(winner))
                    return 1

# Auxiliary function used for CvC moves
def computerplay(game, ai, diff1, diff2, eval):
    if game.turn == 2 and global_method2 == 1:
        tic = time.perf_counter()
        ai.counter = 0
        value, new_board = ai.minimax(game.board, diff2, 2, float('-inf'), float('+inf'), eval)
        toc = time.perf_counter()
        print_stats((round((toc-tic),4)),ai.counter)
        if global_pc1 != 5:
            time.sleep(1)
        game.turn = 1
        eval1 = new_board.evaluationPlayer(1)
        eval2 = new_board.evaluationPlayer(2)
        updateBars(WIN, eval1, eval2)
        game.board = new_board
        game.update()
        winner = game.board.checkWinAndTie()
        if winner >= 0:
            display_message(WIN, str(winner))
            return 1
    elif game.turn == 2 and global_method2 == 2:
        tic = time.perf_counter()
        ai.counter = 0
        value, new_board = ai.minimax_ab(game.board, diff2, 2, float('-inf'), float('+inf'), eval)
        toc = time.perf_counter()
        print_stats((round((toc-tic),4)),ai.counter)
        if global_pc1 != 5:
            time.sleep(1)
        game.turn = 1
        eval1 = new_board.evaluationPlayer(1)
        eval2 = new_board.evaluationPlayer(2)
        updateBars(WIN, eval1, eval2)
        game.board = new_board
        game.update()
        winner = game.board.checkWinAndTie()
        if winner >= 0:
            display_message(WIN, str(winner))
            return 1
    elif game.turn == 1 and global_method1 == 1:
        tic = time.perf_counter()
        ai.counter = 0
        value, new_board = ai.minimax(game.board, diff1, 1, float('-inf'), float('+inf'), eval)
        toc = time.perf_counter()
        print_stats_down((round((toc-tic),4)),ai.counter)
        if global_pc1 != 5:
            time.sleep(1)
        game.turn = 2
        eval1 = new_board.evaluationPlayer(1)
        eval2 = new_board.evaluationPlayer(2)
        updateBars(WIN, eval1, eval2)
        game.board = new_board
        game.update()
        winner = game.board.checkWinAndTie()
        if winner >= 0:
            display_message(WIN, str(winner))
            return 1
    elif game.turn == 1 and global_method1 == 2:
        tic = time.perf_counter()
        ai.counter = 0
        value, new_board = ai.minimax_ab(game.board, diff1, 1, float('-inf'), float('+inf'), eval)
        toc = time.perf_counter()
        print_stats_down((round((toc-tic),4)),ai.counter)
        if global_pc1 != 5:
            time.sleep(1)
        game.turn = 2
        eval1 = new_board.evaluationPlayer(1)
        eval2 = new_board.evaluationPlayer(2)
        updateBars(WIN, eval1, eval2)
        game.board = new_board
        game.update()
        winner = game.board.checkWinAndTie()
        if winner >= 0:
            display_message(WIN, str(winner))
            return 1

# Auxiliary function used for calculating bot hints
def calculateHint(game, ai, WIN, eval):
    for x in range(0,5):
        for y in range(0,5):
            if isinstance(game.board.board[x][y], Move):
                game.board.board[x][y] = 0
    game.update()
    pygame.display.update()
    tic = time.perf_counter()
    ai.counter = 0
    value, new_board = ai.minimax_ab(game.board, 4, game.turn, float('-inf'), float('+inf'), eval)
    toc = time.perf_counter()
    print_stats((round((toc-tic),4)),ai.counter)
    oldBoard = game.board.board_as_string()
    newBoard = new_board.board_as_string()

    selectedPiece = 0
    selectedEnd = 0

    # Updates board
    for x in range(25):
        if oldBoard[x] != newBoard[x]:
            if int(oldBoard[x]) != 0:
                selectedPiece = x
            else:
                selectedEnd = x
    selectedX = selectedPiece // 5
    selectedY = selectedPiece % 5
    selectedEndX = selectedEnd // 5
    selectedEndY = selectedEnd % 5

    # Updates screen
    pygame.draw.rect(WIN, BACKGROUNDGREEN, (175 + selectedY * SQUARE_SIZE, 220 + selectedX * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    if game.turn == 2:
        piece = Piece(selectedX, selectedY, WHITE)
    else:
        piece = Piece(selectedX, selectedY, BLUE)
    piece.draw(WIN)
    pygame.draw.rect(WIN, BACKGROUNDGREEN, (175 + selectedEndY * SQUARE_SIZE, 220 + selectedEndX * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    pygame.display.update()
    time.sleep(1)