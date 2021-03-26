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
        value, new_board, res = ai.minimax(game.board, diff, 2, float('-inf'), float('+inf'), 0)
        eval1 = new_board.evaluationPlayer(1)
        eval2 = new_board.evaluationPlayer(2)
        updateBars(WIN, eval1, eval2)
        game.board = new_board
        game.update()
        winner = game.board.checkWin()
        if (winner > 0):
            drawEnding(winner, 2, WIN)
            display_message(WIN, str(winner))
            return 1
        drawLine(WIN, 1)
        game.turn = 1
    else:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = get_row_col_from_mouse(pos)
            movePlayed = game.select(row, col)
            if (movePlayed == 1):
                eval1 = game.board.evaluationPlayer(1)
                eval2 = game.board.evaluationPlayer(2)
                updateBars(WIN, eval1, eval2)
            game.update()
            winner = game.board.checkWin()
            if (winner > 0): 
                drawEnding(winner, 2, WIN)
                display_message(WIN, str(winner)) 
                return 1

# With Cuts
def method_2(game, ai, event, diff):
    if game.turn == 2:
        value, new_board, res = ai.minimax_ab(game.board, diff, 2, float('-inf'), float('+inf'), 0)
        eval1 = new_board.evaluationPlayer(1)
        eval2 = new_board.evaluationPlayer(2)
        updateBars(WIN, eval1, eval2)
        game.board = new_board
        game.update()
        winner = game.board.checkWin()
        if (winner > 0):
            drawEnding(winner, 2, WIN)
            display_message(WIN, str(winner))
            return 1
        drawLine(WIN, 1)
        game.turn = 1
    else:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = get_row_col_from_mouse(pos)
            movePlayed = game.select(row, col)
            if (movePlayed == 1):
                eval1 = game.board.evaluationPlayer(1)
                eval2 = game.board.evaluationPlayer(2)
                updateBars(WIN, eval1, eval2)
            game.update()
            winner = game.board.checkWin()
            if (winner > 0): 
                drawEnding(winner, 2, WIN)
                display_message(WIN, str(winner)) 
                return 1