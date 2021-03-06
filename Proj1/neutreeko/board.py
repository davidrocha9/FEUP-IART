import pygame
from .constants import BLACK, ROWS, WHITE, PURPLE, BLUE, SQUARE_SIZE, COLS, LIGHTBLUE, GREY
from .piece import Piece
from .move import Move
import random
import time


class Board:
    def __init__(self):
        self.board = [] # Board Matrix
        self.possibleMoves = [] # Stores possible moves for a given player
        self.lastMove = None # Last Move
        self.player1Pieces = [] # PLayer 1 Pieces
        self.player2Pieces = [] # Player 2 Pieces
        self.create_board() # Initializes Board
        self.boards = {} # Map that stores moves in order to check if there is a tie

    # Draws squares for the board
    def draw_squares(self, win):
        for row in range(ROWS):
            for col in range(COLS):
                if (row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1):
                    pygame.draw.rect(win, LIGHTBLUE,
                                     (175 + row * SQUARE_SIZE, 220 + col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(win, BLACK,
                                     (175 + row * SQUARE_SIZE, 220 + col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Assigns Pieces to each players
    def assignPieces(self):
        for x in range(5):
            for y in range(5):
                piece = self.getPiece(x, y)
                if piece != 0:
                    if piece.color == BLUE:
                        self.player1Pieces.append(piece)
                    if piece.color == WHITE:
                        self.player2Pieces.append(piece)

    # Initializes Board
    def create_board(self):
        self.board.append([0, Piece(0, 1, WHITE), 0, Piece(0, 3, WHITE), 0])
        self.board.append([0, 0, Piece(1, 2, BLUE), 0, 0])
        self.board.append([0, 0, 0, 0, 0])
        self.board.append([0, 0, Piece(3, 2, WHITE), 0, 0])
        self.board.append([0, Piece(4, 1, BLUE), 0, Piece(4, 3, BLUE), 0])
        self.assignPieces()

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def getPiece(self, row, col):
        return self.board[row][col]

    # Converts board to a string
    def board_as_string(self):
        result = ""
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == 0:
                    result += "0"
                elif isinstance(self.board[i][j], Piece):
                    if self.board[i][j].color == (255, 255, 255):
                        result += "2"
                    elif self.board[i][j].color == (61, 61, 61):
                        result += "1"
                else:
                    result += "0"
        return result

    # Makes a move
    def move(self, startX, startY, endX, endY, color, player):
        self.board[startX][startY] = 0
        self.board[endX][endY] = Piece(endX, endY, color)
        self.lastMove = endX, endY
        if player == 1:
            for x in range(3):
                if self.player1Pieces[x].row == startX and self.player1Pieces[x].col == startY:
                    self.player1Pieces[x] = self.board[endX][endY]
                    break
        elif player == 2:
            for x in range(3):
                if self.player2Pieces[x].row == startX and self.player2Pieces[x].col == startY:
                    self.player2Pieces[x] = self.board[endX][endY]
                    break

    # Auxiliary functions that checks the surroundings of a piece in all directions
    def checkUp(self, row, col):
        if row == 0 or self.board[row - 1][col] != 0:
            return -1, -1

        while True:
            row = row - 1
            if row < 0:
                break
            elif self.board[row][col] == 0:
                continue
            else:
                break

        row = row + 1

        return row, col

    def checkDown(self, row, col):
        if row == 4 or self.board[row + 1][col] != 0:
            return -1, -1

        while True:
            row = row + 1
            if row > 4:
                break
            elif self.board[row][col] == 0:
                continue
            else:
                break

        row = row - 1

        return row, col

    def checkLeft(self, row, col):
        if col == 0 or self.board[row][col - 1] != 0:
            return -1, -1

        while True:
            col = col - 1
            if (col < 0):
                break
            elif self.board[row][col] == 0:
                continue
            else:
                break

        col = col + 1

        return row, col

    def checkRight(self, row, col):
        if (col == 4 or self.board[row][col + 1] != 0):
            return (-1, -1)

        while True:
            col = col + 1
            if (col > 4):
                break
            elif (self.board[row][col] == 0):
                continue
            else:
                break

        col = col - 1

        return row, col

    def checkUpRight(self, row, col):
        if (col == 4 or row == 0 or self.board[row - 1][col + 1] != 0):
            return (-1, -1)

        while True:
            col = col + 1
            row = row - 1
            if (col > 4 or row < 0):
                break
            elif (self.board[row][col] == 0):
                continue
            else:
                break

        col = col - 1
        row = row + 1

        return row, col

    def checkUpLeft(self, row, col):
        if (col == 0 or row == 0 or self.board[row - 1][col - 1] != 0):
            return (-1, -1)

        while True:
            col = col - 1
            row = row - 1
            if (col < 0 or row < 0):
                break
            elif (self.board[row][col] == 0):
                continue
            else:
                break

        col = col + 1
        row = row + 1

        return row, col

    def checkDownRight(self, row, col):
        if (col == 4 or row == 4 or self.board[row + 1][col + 1] != 0):
            return (-1, -1)

        while True:
            col = col + 1
            row = row + 1
            if (col > 4 or row > 4):
                break
            elif (self.board[row][col] == 0):
                continue
            else:
                break

        col = col - 1
        row = row - 1

        return row, col

    def checkDownLeft(self, row, col):
        if (col == 0 or row == 4 or self.board[row + 1][col - 1] != 0):
            return (-1, -1)

        while True:
            col = col - 1
            row = row + 1
            if (col < 0 or row > 4):
                break
            elif (self.board[row][col] == 0):
                continue
            else:
                break

        col = col + 1
        row = row - 1

        return row, col

    # Returns possible moves for a given state
    def getPossibleMoves(self, row, col):
        possibleMoves = []
        moveRow, moveCol = self.checkUp(row, col)
        if moveRow != -1 and moveCol != -1:
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREY)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkDown(row, col)
        if moveRow != -1 and moveCol != -1:
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREY)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkLeft(row, col)
        if moveRow != -1 and moveCol != -1:
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREY)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkRight(row, col)
        if moveRow != -1 and moveCol != -1:
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREY)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkUpRight(row, col)
        if moveRow != -1 and moveCol != -1:
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREY)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkUpLeft(row, col)
        if moveRow != -1 and moveCol != -1:
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREY)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkDownRight(row, col)
        if moveRow != -1 and moveCol != -1:
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREY)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkDownLeft(row, col)
        if moveRow != -1 and moveCol != -1:
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREY)
            possibleMoves.append((moveRow, moveCol))

        return possibleMoves

    def getAIPossibleMoves(self, row, col):
        possibleMoves = []
        moveRow, moveCol = self.checkUp(row, col)
        if moveRow != -1 and moveCol != -1:
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkDown(row, col)
        if moveRow != -1 and moveCol != -1:
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkLeft(row, col)
        if moveRow != -1 and moveCol != -1:
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkRight(row, col)
        if moveRow != -1 and moveCol != -1:
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkUpRight(row, col)
        if moveRow != -1 and moveCol != -1:
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkUpLeft(row, col)
        if moveRow != -1 and moveCol != -1:
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkDownRight(row, col)
        if moveRow != -1 and moveCol != -1:
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkDownLeft(row, col)
        if moveRow != -1 and moveCol != -1:
            possibleMoves.append((moveRow, moveCol))

        return possibleMoves

    # Checks for 3 in a row
    def check3inARow(self, list):
        pieces = [(list[0].y // SQUARE_SIZE) * 10 + (list[0].x // SQUARE_SIZE),
                  (list[1].y // SQUARE_SIZE) * 10 + (list[1].x // SQUARE_SIZE),
                  (list[2].y // SQUARE_SIZE) * 10 + (list[2].x // SQUARE_SIZE)]
        pieces = sorted(pieces)

        # Direita
        if (pieces[0] + 1 == pieces[1] and pieces[1] + 1 == pieces[2]):
            return True
        # Direita Baixo
        if (pieces[0] + 11 == pieces[1] and pieces[1] + 11 == pieces[2]):
            return True
        # Baixo
        if (pieces[0] + 10 == pieces[1] and pieces[1] + 10 == pieces[2]):
            return True
        # Esquerda Baixo
        if (pieces[0] + 9 == pieces[1] and pieces[1] + 9 == pieces[2]):
            return True

        return False

    # Checks for 2 in a row
    def check2inARow(self, list):
        pieces = []
        eval = 0
        for i in range(3):
            val = (list[i].y // SQUARE_SIZE) * 10 + (list[i].x // SQUARE_SIZE)
            pieces.append(val)

        for i in range(3):
            for x in range(i + 1, 3):
                # Direita
                if (pieces[i] + 1 == pieces[x]):
                    eval += 500
                # Direita Baixo
                if (pieces[i] + 11 == pieces[x]):
                    eval += 500
                # Baixo
                if (pieces[i] + 10 == pieces[x]):
                    eval += 500
                # Esquerda Baixo
                if (pieces[i] + 9 == pieces[x]):
                    eval += 500

        return eval

    # Checks a piece surroundings
    def checkSurrounding(self, list):
        pieces = [(list[0].y // SQUARE_SIZE) * 10 + (list[0].x // SQUARE_SIZE),
                  (list[1].y // SQUARE_SIZE) * 10 + (list[1].x // SQUARE_SIZE),
                  (list[2].y // SQUARE_SIZE) * 10 + (list[2].x // SQUARE_SIZE)]
        pieces = sorted(pieces)
        eval = 0

        # Direita
        if pieces[1] - pieces[0] == 1:
            eval += 10
        if pieces[2] - pieces[1] == 1:
            eval += 10
        if pieces[2] - pieces[0] == 1:
            eval += 10

        # Baixo Direita
        if pieces[1] - pieces[0] == 11:
            eval += 10
        if pieces[2] - pieces[1] == 11:
            eval += 10
        if pieces[2] - pieces[0] == 11:
            eval += 10

        # Baixo
        if pieces[1] - pieces[0] == 10:
            eval += 10
        if pieces[2] - pieces[1] == 10:
            eval += 10
        if pieces[2] - pieces[0] == 10:
            eval += 10

        # Baixo
        if pieces[1] - pieces[0] == 9:
            eval += 10
        if pieces[2] - pieces[1] == 9:
            eval += 10
        if pieces[2] - pieces[0] == 9:
            eval += 10

        return eval

    # Checks if there is 2 pieces in the same row/column/diagonal
    def check2inLine(self, pieces):
        eval = 0

        # Direita
        if pieces[0].row == pieces[1].row:
            eval += 5
        if pieces[0].row == pieces[2].row:
            eval += 5
        if pieces[1].row == pieces[2].row:
            eval += 5

        # Baixo
        if pieces[0].col == pieces[1].col:
            eval += 5
        if pieces[0].col == pieces[2].col:
            eval += 5
        if pieces[1].col == pieces[2].col:
            eval += 5

        # Baixo Direita
        if pieces[1].col - pieces[0].col == pieces[1].row - pieces[0].row:
            eval += 5
        if pieces[2].col - pieces[0].col == pieces[2].row - pieces[0].row:
            eval += 5
        if pieces[2].col - pieces[1].col == pieces[2].row - pieces[1].row:
            eval += 5

        # Baixo Esquerda
        if pieces[0].col - pieces[1].col == pieces[0].row - pieces[1].row:
            eval += 5
        if pieces[0].col - pieces[2].col == pieces[0].row - pieces[2].row:
            eval += 5
        if pieces[1].col - pieces[2].col == pieces[1].row - pieces[2].row:
            eval += 5

        return eval

    def getPiecesCoordinates(self, player):
        if player == 1:
            return self.player1Pieces
        elif player == 2:
            return self.player2Pieces

    # Returns the board evaluation for a specific player
    def evaluationPlayer(self, player):
        eval = 0
        playerPieces = self.getPiecesCoordinates(player)

        # Verificar 3 em linha
        if (self.check3inARow(playerPieces)):
            eval += 5000

        # Verificar 2 em Linha (sem terem que estar adjacentes)
        eval += self.check2inLine(playerPieces)
        eval += self.checkSurrounding(playerPieces)

        return eval

    # Returns the evaluation of the board
    def evaluation(self):
        eval = 0
        player1Pieces = self.getPiecesCoordinates(1)
        player2Pieces = self.getPiecesCoordinates(2)

        # Verificar 3 em linha
        if self.check3inARow(player1Pieces):
            return 5000
        elif self.check3inARow(player2Pieces):
            return -5000

        # Verificar se existe 2 em Linha/Coluna/Diagonal
        # e 2 peças adjacentes
        if 5000 > eval > -5000:
            eval += self.check2inLine(player1Pieces)
            eval -= self.check2inLine(player2Pieces)
            eval += self.checkSurrounding(player1Pieces)
            eval -= self.checkSurrounding(player2Pieces)

        return eval + random.randint(0, 5)

    # Returns a simpler evaluation of the board
    def evaluationOnlyWin(self):
        eval = 0
        player1Pieces = self.getPiecesCoordinates(1)
        player2Pieces = self.getPiecesCoordinates(2)

        # Verificar 3 em linha
        if self.check3inARow(player1Pieces):
            return 5000
        elif self.check3inARow(player2Pieces):
            return -5000

        return eval + random.randint(0, 5)


    def checkPieces(self, list):
        return self.check3inARow(list)

    def checkWin(self):
        player1Pieces = self.getPiecesCoordinates(1)
        player2Pieces = self.getPiecesCoordinates(2)
        if (self.check3inARow(player1Pieces)):
            return 1
        elif (self.check3inARow(player2Pieces)):
            return 2

        return -1

    def checkWinAndTie(self):
        player1Pieces = self.getPiecesCoordinates(1)
        player2Pieces = self.getPiecesCoordinates(2)
        if (self.checkPieces(player1Pieces)):
            return 1
        elif (self.checkPieces(player2Pieces)):
            return 2

        if self.board_as_string() in self.boards.keys():
            self.boards[self.board_as_string()] += 1
        else:
            self.boards.update({self.board_as_string(): 1})

        if (self.boards[self.board_as_string()] == 3):
            return 0

        return -1
