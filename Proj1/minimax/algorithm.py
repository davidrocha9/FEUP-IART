from copy import deepcopy
from neutreeko.constants import SQUARE_SIZE, BLUE, WHITE
import pygame
import time

def minimax(position, depth, player, alpha, beta):
    if depth == 0 or position.checkWin() != -1:
        if (player == 1):
            return position.evaluation() - depth, position
        if (player == 2):
            return position.evaluation() + depth, position

    if player == 1:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, 1):
            evaluation = minimax(move, depth - 1, 2, alpha, beta)[0]
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = move

            if maxEval >= beta:
                return maxEval, best_move
            if maxEval > alpha:
                alpha = maxEval

        return maxEval, best_move
        
    elif player == 2:
        minEval = float('+inf')
        best_move = None
        for move in get_all_moves(position, 2):
            evaluation = minimax(move, depth - 1, 1, alpha, beta)[0]
            if evaluation < minEval:
                minEval = evaluation
                best_move = move
            
            if minEval <= alpha :
                return minEval, best_move

            if minEval < beta:
                beta = minEval

        return minEval, best_move

def simulate_move(piece, move, board, player):
    if (player == 1):
        board.move(piece.row, piece.col, int(move[0]), int(move[1]), BLUE, 1)
    elif (player == 2):
        board.move(piece.row, piece.col, int(move[0]), int(move[1]), WHITE, 2)
    return board
    

def get_all_moves(board, player):
    moves = []

    for piece in board.getPiecesCoordinates(player):
        valid_moves = board.getAIPossibleMoves(piece.row, piece.col)
        for move in valid_moves:
            temp_board = deepcopy(board)
            new_board = simulate_move(piece, move, temp_board, player)
            moves.append(new_board)

    return moves

