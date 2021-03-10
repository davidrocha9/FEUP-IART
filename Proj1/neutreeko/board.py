import pygame
from .constants import BLACK, ROWS, RED, GREEN, BLUE, SQUARE_SIZE, COLS, WHITE
from .piece import Piece
from .move import Move

class Board:
    def __init__(self):
        self.board = []
        self.possibleMoves = []
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, WHITE, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        self.board.append([0, Piece(0, 1, RED), 0, Piece(0, 3, RED), 0])
        self.board.append([0, 0, Piece(1, 2, BLUE), 0, 0])
        self.board.append([0, 0, 0, 0, 0])
        self.board.append([0, 0, Piece(3, 2, RED), 0, 0])
        self.board.append([0, Piece(4, 1, BLUE), 0, Piece(4, 3, BLUE), 0])

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def getPiece(self, row, col):
        return self.board[row][col]
    
    def checkUp(self, row, col):
        if (row == 0 or self.board[row-1][col] != 0):
            return (-1,-1)

        while True:
            row = row - 1
            if (row < 0):
                break
            elif (self.board[row][col] == 0):
                continue
            else: break
        
        row = row + 1

        return row, col

    def checkDown(self, row, col):
        if (row == 4 or self.board[row+1][col] != 0):
            return (-1,-1)

        while True:
            row = row + 1
            if (row > 4):
                break
            elif (self.board[row][col] == 0):
                continue
            else: break
        
        row = row - 1

        return row, col

    def checkLeft(self, row, col):
        if (col == 0 or self.board[row][col-1] != 0):
            return (-1,-1)

        while True:
            col = col - 1
            if (col < 0):
                break
            elif (self.board[row][col] == 0):
                continue
            else: break
        
        col = col + 1

        return row, col

    def checkRight(self, row, col):
        if (col == 4 or self.board[row][col+1] != 0):
            return (-1,-1)

        while True:
            col = col + 1
            if (col > 4):
                break
            elif (self.board[row][col] == 0):
                continue
            else: break
        
        col = col - 1

        return row, col

    def checkUpRight(self, row, col):
        if (col == 4 or row == 0 or self.board[row-1][col+1] != 0):
            return (-1,-1)

        while True:
            col = col + 1
            row = row - 1
            if (col > 4 or row < 0):
                break
            elif (self.board[row][col] == 0):
                continue
            else: break
        
        col = col - 1
        row = row + 1

        return row, col   

    def checkUpLeft(self, row, col):
        if (col == 0 or row == 0 or self.board[row-1][col-1] != 0):
            return (-1,-1)

        while True:
            col = col - 1
            row = row - 1
            if (col < 0 or row < 0):
                break
            elif (self.board[row][col] == 0):
                continue
            else: break
        
        col = col + 1
        row = row + 1

        return row, col

    def checkDownRight(self, row, col):
        if (col == 4 or row == 4 or self.board[row+1][col+1] != 0):
            return (-1,-1)

        while True:
            col = col + 1
            row = row + 1
            if (col > 4 or row > 4):
                break
            elif (self.board[row][col] == 0):
                continue
            else: break
        
        col = col - 1
        row = row - 1

        return row, col   

    def checkDownLeft(self, row, col):
        if (col == 0 or row == 4 or self.board[row+1][col-1] != 0):
            return (-1,-1)

        while True:
            col = col - 1
            row = row + 1
            if (col < 0 or row > 4):
                break
            elif (self.board[row][col] == 0):
                continue
            else: break
        
        col = col + 1
        row = row - 1

        return row, col 

    def getPossibleMoves(self, row, col, win):
        possibleMoves=[]
        moveRow, moveCol = self.checkUp(row, col)
        if (moveRow != -1 and moveCol != -1):
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREEN)
            possibleMoves.append((moveRow, moveCol))
        
        moveRow, moveCol = self.checkDown(row, col)
        if (moveRow != -1 and moveCol != -1):
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREEN)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkLeft(row, col)
        if (moveRow != -1 and moveCol != -1):
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREEN)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkRight(row, col)
        if (moveRow != -1 and moveCol != -1):
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREEN)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkUpRight(row, col)
        if (moveRow != -1 and moveCol != -1):
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREEN)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkUpLeft(row, col)
        if (moveRow != -1 and moveCol != -1):
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREEN)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkDownRight(row, col)
        if (moveRow != -1 and moveCol != -1):
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREEN)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkDownLeft(row, col)
        if (moveRow != -1 and moveCol != -1):
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREEN)
            possibleMoves.append((moveRow, moveCol))

        return possibleMoves
        
