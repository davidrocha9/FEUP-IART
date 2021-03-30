from utils import *


# Without cuts
def method_1(game, ai, event, diff):
    if game.turn == 2:
        new_board = None
        value, new_board = ai.minimax(game.board, diff, 2, float('-inf'), float('+inf'))
        game.turn = 1
        eval1 = new_board.evaluationPlayer(1)
        eval2 = new_board.evaluationPlayer(2)
        updateBars(WIN, eval1, eval2)
        game.board = new_board
        game.update()
        winner = game.board.checkWin()
        if winner >= 0:
            drawEnding(winner, diff, WIN)
            display_message(WIN, str(winner))
            return 1
        drawLine(WIN, diff)
    else:
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
                winner = game.board.checkWin()
                if winner >= 0:
                    drawEnding(winner, diff, WIN)
                    display_message(WIN, str(winner))
                    return 1


# With Cuts
def method_2(game, ai, event, diff):
    if game.turn == 2:
        new_board = None
        value, new_board = ai.minimax_ab(game.board, diff, 2, float('-inf'), float('+inf'))
        game.turn = 1
        eval1 = new_board.evaluationPlayer(1)
        eval2 = new_board.evaluationPlayer(2)
        updateBars(WIN, eval1, eval2)
        game.board = new_board
        game.update()
        winner = game.board.checkWin()
        if winner >= 0:
            drawEnding(winner, diff, WIN)
            display_message(WIN, str(winner))
            return 1
        drawLine(WIN, diff)
    else:
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
                winner = game.board.checkWin()
                if winner >= 0:
                    drawEnding(winner, diff, WIN)
                    display_message(WIN, str(winner))
                    return 1


# With Cuts
def method_3(game, ai, event, diff):
    if game.turn == 2:
        new_board = None
        while new_board is None or new_board.board == game.board.board:
            value, new_board = ai.negamax(game.board, diff, 2, float('-inf'), float('+inf'))
        game.turn = 1
        eval1 = new_board.evaluationPlayer(1)
        eval2 = new_board.evaluationPlayer(2)
        updateBars(WIN, eval1, eval2)
        game.board = new_board
        game.update()
        winner = game.board.checkWin()
        if winner >= 0:
            drawEnding(winner, diff, WIN)
            display_message(WIN, str(winner))
            return 1
        drawLine(WIN, diff)
    else:
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
                winner = game.board.checkWin()
                if winner >= 0:
                    drawEnding(winner, diff, WIN)
                    display_message(WIN, str(winner))
                    return 1