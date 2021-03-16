import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from neutreeko.board import Board
from .piece import Piece
from .move import Move

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = 1
        self.player1Pieces = []
        self.player2Pieces = []
        self.currentPossibleMoves = []

    def updateBoard(self, startX, startY, endX, endY, color):
        self.board.board[startX][startY] = 0
        self.board.board[endX][endY] = Piece(endX, endY, color)

    def select(self, row, col):
        self.player1Pieces = self.getPiecesCoordinates(1)
        self.player2Pieces = self.getPiecesCoordinates(2)

        if (self.selected):
            if (self.turn == 1):
                for i in self.player1Pieces:
                    if ((i.y // SQUARE_SIZE,i.x // SQUARE_SIZE) == (row,col)):
                        self.selected = None
                        for pair in self.currentPossibleMoves:
                            if (pair == (row, col)):
                                continue
                            else:
                                self.board.board[pair[0]][pair[1]] = 0
            else:
                for i in self.player2Pieces:
                    if ((i.y // SQUARE_SIZE,i.x // SQUARE_SIZE) == (row,col)):
                        self.selected = None
                        for pair in self.currentPossibleMoves:
                            if (pair == (row, col)):
                                continue
                            else:
                                self.board.board[pair[0]][pair[1]] = 0

        if (self.selected is None):
            if (self.turn == 1):
                for piece in self.player1Pieces:
                    pieceRow = piece.y // SQUARE_SIZE
                    pieceCol = piece.x // SQUARE_SIZE

                    if (row == pieceRow and col == pieceCol):
                        self.selected = self.board.getPiece(row, col)
                        self.currentPossibleMoves = self.board.getPossibleMoves(row, col, self.win)          
            else:
                for piece in self.player2Pieces:
                    pieceRow = piece.y // SQUARE_SIZE
                    pieceCol = piece.x // SQUARE_SIZE

                    if (row == pieceRow and col == pieceCol):
                        self.selected = self.board.getPiece(row, col)
                        self.currentPossibleMoves = self.board.getPossibleMoves(row, col, self.win)
        else:
            selectedY = SQUARE_SIZE * col + SQUARE_SIZE // 2 
            selectedX = SQUARE_SIZE * row + SQUARE_SIZE // 2
            
            startX = self.selected.y // SQUARE_SIZE
            startY = self.selected.x // SQUARE_SIZE

            endX = selectedX // SQUARE_SIZE
            endY = selectedY // SQUARE_SIZE

            if ((endX, endY) in self.currentPossibleMoves):
                if (self.turn == 1):            
                    self.updateBoard(startX, startY, endX, endY, BLUE)
                else:
                    self.updateBoard(startX, startY, endX, endY, RED)

                self.selected = None
                self.turn = 1 + (self.turn % 2)
                for pair in self.currentPossibleMoves:
                    if (pair == (endX, endY)):
                        continue
                    else:
                        self.board.board[pair[0]][pair[1]] = 0

    def getPiecesCoordinates(self, player):
        pattern = BLUE
        if (player == 2):
            pattern = RED
        
        result = []
        for x in range(5):
            for y in range(5):
                piece = self.board.getPiece(x,y)
                if (piece != 0):
                    if (piece.color == pattern):
                        result.append(piece)
        return result

    def checkPieces(self, list):
        pieces = []
        for i in range(3):
            val = (list[i].x // SQUARE_SIZE) * 10 + (list[i].y // SQUARE_SIZE)
            pieces.append(val)
        
        if (pieces[0] + 10 == pieces[1] and pieces[1] + 10 == pieces[2]):
            return True
        if (pieces[0] + 1 == pieces[1] and pieces[1] + 1 == pieces[2]):
            return True    
        if (pieces[0] + 11 == pieces[1] and pieces[1] + 11 == pieces[2]):
            return True    
        if (pieces[0] - 9 == pieces[2] and pieces[1] - 9 == pieces[2]):
            return True
        
        return False

    def checkWin(self):
        player1Pieces = self.getPiecesCoordinates(1)
        player2Pieces = self.getPiecesCoordinates(2)
        
        if (self.checkPieces(player1Pieces)):
            print("Player 1 Wins!")
            return 1
        elif (self.checkPieces(player2Pieces)):
            print("Player 2 Wins!")
            return 2
    
        return 0 

    def update(self):
        self.board.draw(self.win)
        pygame.display.update()

    """
    Funcao de analise:
    Resultado = Pontos do Jogador 1 - Pontos do Jogador 2

    Atribuicao de Pontos:

    Mate em 1 - 100 pontos
    Impedir Mate em 1 do Adversario - 50 pontos
    Fazer 2 em linha - 20 pontos
    Impedir 2 em linha do Adversario - 10 pontos
    Peca a uma casa de distancia de outra Peca - 2 pontos
    Peca a duas casas de distancia de outra Peca - 1 ponto
    

    """

        