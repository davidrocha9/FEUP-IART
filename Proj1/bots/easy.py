import pygame
from pygame import gfxdraw
import pygame_menu
import time
from neutreeko.constants import *
from neutreeko.game import Game
from minimax.algorithm import AI
import time
import random
from utils import *

# Without cuts
def method_1(game, ai, event, diff):
    if game.turn == 2:
        value, new_board = ai.minimax(game.board, 1, 2, float('-inf'), float('+inf'))
        print(value)
        eval1 = new_board.evaluationPlayer(1)
        eval2 = new_board.evaluationPlayer(2)
        updateBars(WIN, eval1, eval2)
        game.board = new_board
        game.update()
        winner = game.board.checkWin()
        if (winner >= 0):
            drawEnding(winner, diff, WIN)
            display_message(WIN, str(winner))
            return 1
        drawLine(WIN, diff)
        game.turn = 1
    else:
        if event.type == pygame.KEYDOWN:
            if event.unicode == 'h':
                value, new_board, res = ai.minimax_ab(game.board, 5, 1, float('-inf'), float('+inf'))
                eval1 = new_board.evaluationPlayer(1)
                eval2 = new_board.evaluationPlayer(2)
                updateBars(WIN, eval1, eval2)
                game.board = new_board
                game.update()
                winner = game.board.checkWin()
                if (winner >= 0):
                    drawEnding(winner, diff, WIN)
                    display_message(WIN, str(winner))
                    return 1
                drawLine(WIN, diff)
                game.turn = 2
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = get_row_col_from_mouse(pos)
            movePlayed = game.select(row, col)
            if (movePlayed == 1):
                eval1 = game.board.evaluationPlayer(1)
                eval2 = game.board.evaluationPlayer(2)
                updateBars(WIN, eval1, eval2)
                game.update()
                winner = game.board.checkWin()
                if (winner >= 0): 
                    drawEnding(winner, diff, WIN)
                    display_message(WIN, str(winner)) 
                    return 1

# With Cuts
def method_2(game, ai, event, diff):
    if game.turn == 2:
        value, new_board = ai.minimax_ab(game.board, diff, 2, float('-inf'), float('+inf'))
        eval1 = new_board.evaluationPlayer(1)
        eval2 = new_board.evaluationPlayer(2)
        updateBars(WIN, eval1, eval2)
        game.board = new_board
        game.update()
        winner = game.board.checkWin()
        if (winner >= 0):
            drawEnding(winner, diff, WIN)
            display_message(WIN, str(winner))
            return 1
        drawLine(WIN, diff)
        game.turn = 1
    else:
        if event.type == pygame.KEYDOWN:
            if event.unicode == 'h':
                value, new_board, res = ai.minimax_ab(game.board, 5, 1, float('-inf'), float('+inf'))
                eval1 = new_board.evaluationPlayer(1)
                eval2 = new_board.evaluationPlayer(2)
                updateBars(WIN, eval1, eval2)
                game.board = new_board
                game.update()
                winner = game.board.checkWin()
                if (winner >= 0):
                    drawEnding(winner, diff, WIN)
                    display_message(WIN, str(winner))
                    return 1
                drawLine(WIN, diff)
                game.turn = 2
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = get_row_col_from_mouse(pos)
            movePlayed = game.select(row, col)
            if (movePlayed == 1):
                eval1 = game.board.evaluationPlayer(1)
                eval2 = game.board.evaluationPlayer(2)
                updateBars(WIN, eval1, eval2)
                game.update()
                winner = game.board.checkWin()
                if (winner >= 0): 
                    drawEnding(winner, diff, WIN)
                    display_message(WIN, str(winner)) 
                    return 1