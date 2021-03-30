import pygame
from .constants import BLACK, ROWS, WHITE, PURPLE, BLUE, SQUARE_SIZE, COLS, LIGHTBLUE, GREY
from .piece import Piece
from .move import Move
import random
import time

class Board:
    def __init__(self):
        self.board = []
        self.possibleMoves = []
        self.lastMove = None
        self.player1Pieces = []
        self.player2Pieces = []
        self.create_board()
        self.boards={}

    def draw_squares(self, win):
        for row in range(ROWS):
            for col in range(COLS):
                if ((row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1)):
                    pygame.draw.rect(win, LIGHTBLUE, (175 + row*SQUARE_SIZE, 220 + col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(win, BLACK, (175 + row*SQUARE_SIZE, 220 + col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def assignPieces(self):
        for x in range(5):
            for y in range(5):
                piece = self.getPiece(x,y)
                if (piece != 0):
                    if (piece.color == BLUE):
                        self.player1Pieces.append(piece)
                    if (piece.color == WHITE):
                        self.player2Pieces.append(piece)

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
    
    def board_as_string(self):
        result = ""
        for i in range(5):
            for j in range(5):
                if(self.board[i][j] == 0):
                        result += "0"
                elif (isinstance(self.board[i][j],Piece)):
                    if(self.board[i][j].color == (255,255,255)):
                        result += "2"
                    elif(self.board[i][j].color == (61,61,61)):
                        result += "1" 
                else:
                    result += "0"
        return result

    def move(self, startX, startY, endX, endY, color, player):
        self.board[startX][startY] = 0
        self.board[endX][endY] = Piece(endX, endY, color)
        self.lastMove = endX, endY
        if (player == 1):
            for x in range(3):
                if (self.player1Pieces[x].row == startX and self.player1Pieces[x].col == startY):
                    self.player1Pieces[x] = self.board[endX][endY]
                    break
        elif (player == 1):
            for x in range(3):
                if (self.player2Pieces[x].row == startX and self.player2Pieces[x].col == startY):
                    self.player2Pieces[x] = self.board[endX][endY]
                    break
                
                
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

    def getPossibleMoves(self, row, col):
        possibleMoves=[]
        moveRow, moveCol = self.checkUp(row, col)
        if (moveRow != -1 and moveCol != -1):
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREY)
            possibleMoves.append((moveRow, moveCol))
        
        moveRow, moveCol = self.checkDown(row, col)
        if (moveRow != -1 and moveCol != -1):
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREY)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkLeft(row, col)
        if (moveRow != -1 and moveCol != -1):
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREY)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkRight(row, col)
        if (moveRow != -1 and moveCol != -1):
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREY)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkUpRight(row, col)
        if (moveRow != -1 and moveCol != -1):
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREY)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkUpLeft(row, col)
        if (moveRow != -1 and moveCol != -1):
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREY)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkDownRight(row, col)
        if (moveRow != -1 and moveCol != -1):
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREY)
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkDownLeft(row, col)
        if (moveRow != -1 and moveCol != -1):
            self.board[moveRow][moveCol] = Move(moveRow, moveCol, GREY)
            possibleMoves.append((moveRow, moveCol))

        return possibleMoves

    def getAIPossibleMoves(self, row, col):
        possibleMoves=[]
        moveRow, moveCol = self.checkUp(row, col)
        if (moveRow != -1 and moveCol != -1):
            possibleMoves.append((moveRow, moveCol))
        
        moveRow, moveCol = self.checkDown(row, col)
        if (moveRow != -1 and moveCol != -1):
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkLeft(row, col)
        if (moveRow != -1 and moveCol != -1):
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkRight(row, col)
        if (moveRow != -1 and moveCol != -1):
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkUpRight(row, col)
        if (moveRow != -1 and moveCol != -1):
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkUpLeft(row, col)
        if (moveRow != -1 and moveCol != -1):
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkDownRight(row, col)
        if (moveRow != -1 and moveCol != -1):
            possibleMoves.append((moveRow, moveCol))

        moveRow, moveCol = self.checkDownLeft(row, col)
        if (moveRow != -1 and moveCol != -1):
            possibleMoves.append((moveRow, moveCol))

        return possibleMoves
    
    def check3inARow(self, list):
        pieces = []
        for i in range(3):
            val = (list[i].y // SQUARE_SIZE) * 10 + (list[i].x // SQUARE_SIZE)
            pieces.append(val)
        
        #Direita
        if (pieces[0] + 1 == pieces[1] and pieces[1] + 1 == pieces[2]):
            return True
        #Direita Baixo
        if (pieces[0] + 11 == pieces[1] and pieces[1] + 11 == pieces[2]):
            return True
        #Baixo
        if (pieces[0] + 10 == pieces[1] and pieces[1] + 10 == pieces[2]):
            return True
        #Esquerda Baixo
        if (pieces[0] + 9 == pieces[1] and pieces[1] + 9 == pieces[2]):
            return True

        return False

    def check2inARow(self, list):
        pieces = []
        eval = 0
        for i in range(3):
            val = (list[i].y // SQUARE_SIZE) * 10 + (list[i].x // SQUARE_SIZE)
            pieces.append(val)

        for i in range(3):
            for x in range(i+1, 3):
                #Direita
                if (pieces[i] + 1 == pieces[x]):
                    eval += 500
                #Direita Baixo
                if (pieces[i] + 11 == pieces[x]):
                    eval += 500
                #Baixo
                if (pieces[i] + 10 == pieces[x]):
                    eval += 500
                #Esquerda Baixo
                if (pieces[i] + 9 == pieces[x]):
                    eval += 500

        return eval

    def checkSurrounding(self, pieces):
        eval = 0
        for piece in pieces:
            #Cima
            if (piece.row > 0):
                if (self.board[piece.row-1][piece.col] != 0):
                    eval += 1
                #Cima Esquerda
                if (piece.col > 0):
                    if (self.board[piece.row-1][piece.col - 1] != 0):
                        eval += 1
                #Cima Direita
                if (piece.col < 4):
                    if (self.board[piece.row-1][piece.col + 1] != 0):
                        eval += 1
            #Baixo
            if (piece.row < 4):
                if (self.board[piece.row+1][piece.col] != 0):
                    eval += 1
                #Baixo Esquerda
                if (piece.col > 0):
                    if (self.board[piece.row + 1][piece.col - 1] != 0):
                        eval += 1
                #Baixo Direita
                if (piece.col < 4):
                    if (self.board[piece.row + 1][piece.col + 1] != 0):
                        eval += 1
            #Esquerda
            if (piece.col > 0):
                if (self.board[piece.row][piece.col-1] != 0):
                    eval += 1
            #Direita
            if (piece.col < 4):
                if (self.board[piece.row][piece.col+1] != 0):
                    eval += 1
        
        return eval

    def check2inLine(self, list):
        pieces = []
        eval = 0
        for i in range(3):
            val = (list[i].y // SQUARE_SIZE) * 10 + (list[i].x // SQUARE_SIZE)
            pieces.append(val)

        #Direita
        for i in range(0,5):
            if (pieces[0] + i == pieces[1]):
                eval += 5
            if (pieces[0] + i == pieces[1]):
                eval += 5
            if (pieces[0] + i == pieces[2]):
                eval += 5
        
        #Baixo Direita
        for i in range(0,50,11):
            if (pieces[0] + i == pieces[1]):
                eval += 5
            if (pieces[0] + i == pieces[1]):
                eval += 5
            if (pieces[0] + i == pieces[2]):
                eval += 5

        #Baixo
        for i in range(0,50,10):
            if (pieces[0] + i == pieces[1]):
                eval += 5
            if (pieces[0] + i == pieces[1]):
                eval += 5
            if (pieces[0] + i == pieces[2]):
                eval += 5
        
        #Baixo Esquerda
        for i in range(0,50,9):
            if (pieces[0] + i == pieces[1]):
                eval += 5
            if (pieces[0] + i == pieces[1]):
                eval += 5
            if (pieces[0] + i == pieces[2]):
                eval += 5

        return eval
                
    def getPiecesCoordinates(self, player):
        pattern = BLUE
        if (player == 2):
            pattern = WHITE
        
        result = []
        for x in range(5):
            for y in range(5):
                piece = self.getPiece(x,y)
                if (piece != 0):
                    if (piece.color == pattern):
                        result.append(piece)
        return result

    def evaluationPlayer(self, player):
        eval = 0
        playerPieces = self.getPiecesCoordinates(player)

        #Verificar 3 em linha
        if (self.check3inARow(playerPieces)):
            eval += 5000

        #Verificar 2 em Linha (sem terem que estar adjacentes)
        eval += self.check2inLine(playerPieces)
        eval += self.checkSurrounding(playerPieces)

        return eval

    def evaluation(self):
        eval = 0
        player1Pieces = self.getPiecesCoordinates(1)
        player2Pieces = self.getPiecesCoordinates(2)

        #Verificar 3 em linha
        if (self.check3inARow(player1Pieces)):
            eval += 5000
        if (self.check3inARow(player2Pieces)):
            eval -= 5000

        if (self.check2inLine(player1Pieces)):
            eval += 5000
        if (self.check2inLine(player2Pieces)):
            eval -= 5000

        return eval

    def checkPieces(self, list):          
        return self.check3inARow(list)
    
    def checkWin(self):
        player1Pieces = self.getPiecesCoordinates(1)
        player2Pieces = self.getPiecesCoordinates(2)
        if (self.checkPieces(player1Pieces)):
            return 1
        elif (self.checkPieces(player2Pieces)):
            return 2

        if self.board_as_string() in self.boards.keys():
            self.boards[self.board_as_string()] += 1
        else:
            self.boards.update({self.board_as_string() : 1})
        
        if (self.boards[self.board_as_string()] == 3):
            return 0
        
        return -1

