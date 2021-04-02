import pygame
from .constants import WHITE, BLUE, SQUARE_SIZE
from neutreeko.board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = 1
        self.player1Pieces = []
        self.player2Pieces = []
        self.currentPossibleMoves = []
        self.pressedHint = False
        self.p1HintCounter = 0
        self.p2HintCounter = 0

    # Used for selecting piece to play and square to move to
    def select(self, row, col):
        self.player2Pieces = self.board.getPiecesCoordinates(2)
        self.player1Pieces = self.board.getPiecesCoordinates(1)
        # Changing selected piece
        if self.turn == 1:
            for i in self.player1Pieces:
                if (i.y // SQUARE_SIZE, i.x // SQUARE_SIZE) == (row, col):
                    self.selected = None
                    for pair in self.currentPossibleMoves:
                        if pair == (row, col):
                            continue
                        else:
                            self.board.board[pair[0]][pair[1]] = 0
        else:
            for i in self.player2Pieces:
                if (i.y // SQUARE_SIZE, i.x // SQUARE_SIZE) == (row, col):
                    self.selected = None
                    for pair in self.currentPossibleMoves:
                        if pair == (row, col):
                            continue
                        else:
                            self.board.board[pair[0]][pair[1]] = 0
        # Selecting piece for first time
        if self.selected is None:
            if self.turn == 1:
                for piece in self.player1Pieces:
                    pieceRow = piece.y // SQUARE_SIZE
                    pieceCol = piece.x // SQUARE_SIZE

                    if row == pieceRow and col == pieceCol:
                        self.selected = self.board.getPiece(row, col)
                        self.currentPossibleMoves = self.board.getPossibleMoves(row, col)          
            else:
                for piece in self.player2Pieces:
                    pieceRow = piece.y // SQUARE_SIZE
                    pieceCol = piece.x // SQUARE_SIZE

                    if row == pieceRow and col == pieceCol:
                        self.selected = self.board.getPiece(row, col)
                        self.currentPossibleMoves = self.board.getPossibleMoves(row, col)
        # Making the move
        else:
            selectedY = SQUARE_SIZE * col + SQUARE_SIZE // 2 
            selectedX = SQUARE_SIZE * row + SQUARE_SIZE // 2
            
            startX = self.selected.y // SQUARE_SIZE
            startY = self.selected.x // SQUARE_SIZE

            endX = selectedX // SQUARE_SIZE
            endY = selectedY // SQUARE_SIZE

            if (endX, endY) in self.currentPossibleMoves:
                if self.turn == 1:
                    self.board.move(startX, startY, endX, endY, BLUE, 1)
                else:
                    self.board.move(startX, startY, endX, endY, WHITE, 2)

                self.selected = None
                self.turn = 1 + (self.turn % 2)
                for pair in self.currentPossibleMoves:
                    if (pair == (endX, endY)):
                        continue
                    else:
                        self.board.board[pair[0]][pair[1]] = 0
                return 1
        
    # Updates game state
    def update(self):
        self.board.draw(self.win)
        pygame.display.update()
