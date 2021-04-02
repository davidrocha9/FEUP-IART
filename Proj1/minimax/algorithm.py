from copy import deepcopy
from neutreeko.constants import SQUARE_SIZE, BLUE, WHITE
import pygame
import time


class AI:
    def __init__(self):
        self.counter = 0
        self.functionToUse = 0

    # Basic Minimax
    def minimax(self, position, depth, player, alpha, beta, eval):
        self.functionToUse = eval
        print(self.functionToUse)
        if depth == 0 or position.checkWin() != -1:
            self.counter += 1
            if player == 1:
                if eval == 1:
                    return position.evaluationOnlyWin() - depth, position
                else:
                    return position.evaluation() - depth, position
            if player == 2:
                if eval == 1:
                    return position.evaluationOnlyWin() + depth, position
                else:
                    return position.evaluation() + depth, position

        if player == 1:
            maxEval = float('-inf')
            best_move = None
            for move in self.get_all_moves(position, 1):
                evaluation = self.minimax(move, depth - 1, 2, alpha, beta, eval)[0]
                if evaluation > maxEval:
                    maxEval = evaluation
                    best_move = move

            return maxEval, best_move

        elif player == 2:
            minEval = float('+inf')
            best_move = None
            for move in self.get_all_moves(position, 2):
                evaluation = self.minimax_ab(move, depth - 1, 1, alpha, beta, eval)[0]
                if evaluation < minEval:
                    minEval = evaluation
                    best_move = move

            return minEval, best_move

    # Minimax with cuts
    def minimax_ab(self, position, depth, player, alpha, beta, eval):
        if depth == 0 or position.checkWin() != -1:
            self.counter += 1
            if player == 1:
                if eval == 1:
                    return position.evaluationOnlyWin() - depth, position
                else:
                    return position.evaluation() - depth, position
            if player == 2:
                if eval == 1:
                    return position.evaluationOnlyWin() + depth, position
                else:
                    return position.evaluation() + depth, position

        if player == 1:
            maxEval = float('-inf')
            best_move = None
            for move in self.get_all_moves(position, 1):
                evaluation = self.minimax_ab(move, depth - 1, 2, alpha, beta, eval)[0]
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
            for move in self.get_all_moves(position, 2):
                evaluation = self.minimax_ab(move, depth - 1, 1, alpha, beta, eval)[0]
                if evaluation < minEval:
                    minEval = evaluation
                    best_move = move

                if minEval <= alpha:
                    return minEval, best_move

                if minEval < beta:
                    beta = minEval

            return minEval, best_move

    # Creates the board given a move
    def simulate_move(self, piece, move, board, player):
        if player == 1:
            board.move(piece.row, piece.col, int(move[0]), int(move[1]), BLUE, 1)
        elif player == 2:
            board.move(piece.row, piece.col, int(move[0]), int(move[1]), WHITE, 2)
        return board

    # Sorts Moves based on the chosen evaluation function
    def sortMoves(self, moves):
        if self.functionToUse == 1:
            return moves.evaluationOnlyWin()
        else:
            return moves.evaluation()

    # Retrieves all possible boards for a given set of moves
    def get_all_moves(self, board, player):
        moves = []
        for piece in board.getPiecesCoordinates(player):
            valid_moves = board.getAIPossibleMoves(piece.row, piece.col)
            for move in valid_moves:
                temp_board = deepcopy(board)
                new_board = self.simulate_move(piece, move, temp_board, player)
                moves.append(new_board)

        moves = sorted(moves, key=self.sortMoves, reverse=True)
        return moves
