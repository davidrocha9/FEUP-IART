from collections import namedtuple

plyr1 = " X "
plyr2 = " O "
empty = "   "

board = [[empty, plyr2, empty, plyr2, empty],
         [empty, empty, plyr1, empty, empty],
         [empty, empty, empty, empty, empty],
         [empty, empty, plyr2, empty, empty],
         [empty, plyr1, empty, plyr1, empty]]


def draw_menu():
    print("Welcome to Neutreeko\nSelect your preferred game mode")
    print("")
    print("1 - Player VS Player\n2 - Player VS PC\n3 - PC VS PC")
    done = True
    while (done):
        mode = input("Option:")
        if (mode.isdigit() and (int(mode) > 0 and int(mode) < 4)):
            return int(mode)
        else:
            print("Invalid Option. Try again.")
            
    

def drawBoard():
    print("     A   B   C   D   E  ")
    print("   ---------------------")
    for x in range(5):
        line = " " + str(x + 1) + " |"
        for y in range (5):
            line += board[x][y]
            line += "|"
        print(line)
        print("   ---------------------")
            
letters = {
  "a": 0,
  "A": 0,
  "b": 1,
  "B": 1,
  "c": 2,
  "C": 2,
  "d": 3,
  "D": 3,
  "e": 4,
  "E": 4,
}
        
def getPiecesCoordinates(player):
    pattern = " X "
    if (player == 2):
        pattern = " O "
    elif (player == "emptySquare"):
        pattern = "   "
    
    result = []
    for x in range(5):
        for y in range(5):
            if (board[x][y] == pattern):
                result.append(str(y*10 + x).zfill(2))
    return result

    
def replaceUp(player, startCoordinates):
    x = int(startCoordinates[0])
    y = int(startCoordinates[1])
    if (y == 0 or board[y - 1][x] != "   "):
        print("Cant move up!")
        return move(player, x)
    
    done = 1
    while(done == 1):
        y = y - 1
        if (y < 0):
            done = 0
        elif (board[y][x] == "   "):
            continue
        else: done = 0
        
    y = y + 1
        
    return x,y

def replaceDown(player, startCoordinates):
    x = int(startCoordinates[0])
    y = int(startCoordinates[1])    
    if (y == 4 or board[y + 1][x] != "   "):
        print("Cant move down!")
        return move(player, startCoordinates)
    
    done = 1
    while(done == 1):
        y = y + 1
        if (y > 4):
            done = 0
        elif (board[y][x] == "   "):
            continue
        else: done = 0
        
    y = y - 1
        
    return x,y

def replaceLeft(player, startCoordinates):
    x = int(startCoordinates[0])
    y = int(startCoordinates[1])    
    if (x == 0 or board[y][x - 1] != "   "):
        print("Cant move left!")
        return move(player, startCoordinates)
    
    done = 1
    while(done == 1):
        x = x - 1
        if (x < 0):
            done = 0
        elif (board[y][x] == "   "):
            continue
        else: done = 0
        
    x = x + 1
        
    return x,y
    
def replaceRight(player, startCoordinates):
    x = int(startCoordinates[0])
    y = int(startCoordinates[1])    
    if (x == 4 or board[y][x + 1] != "   "):
        print("Cant move right!")
        return move(player, startCoordinates)
    
    done = 1
    while(done == 1):
        x = x + 1
        if (x > 4):
            done = 0
        elif (board[y][x] == "   "):
            continue
        else: done = 0
        
    x = x - 1
    return x,y
    
def replaceUpRight(player, startCoordinates):
    x = int(startCoordinates[0])
    y = int(startCoordinates[1])
    if (y == 0 or x == 4 or board[y - 1][x + 1] != "   "):
        print("Cant move up right!")
        return move(player, x)
    
    done = 1
    while(done == 1):
        y = y - 1
        x = x + 1
        if (y < 0 or x > 4):
            done = 0
        elif (board[y][x] == "   "):
            continue
        else: done = 0
        
    y = y + 1
    x = x - 1
        
    return x,y

def replaceUpLeft(player, startCoordinates):
    x = int(startCoordinates[0])
    y = int(startCoordinates[1])
    if (y == 0 or x == 0 or board[y - 1][x - 1] != "   "):
        print("Cant move up left!")
        return move(player, x)
    
    done = 1
    while(done == 1):
        y = y - 1
        x = x - 1
        if (y < 0 or x < 0):
            done = 0
        elif (board[y][x] == "   "):
            continue
        else: done = 0
        
    y = y + 1
    x = x + 1
        
    return x,y

def replaceDownRight(player, startCoordinates):
    x = int(startCoordinates[0])
    y = int(startCoordinates[1])
    if (y == 4 or x == 4 or board[y + 1][x + 1] != "   "):
        print("Cant move down right!")
        return move(player, x)
    
    done = 1
    while(done == 1):
        y = y + 1
        x = x + 1
        if (y > 4 or x > 4):
            done = 0
        elif (board[y][x] == "   "):
            continue
        else: done = 0
        
    y = y - 1
    x = x - 1
        
    return x,y

def replaceDownLeft(player, startCoordinates):
    x = int(startCoordinates[0])
    y = int(startCoordinates[1])
    if (y == 4 or x == 0 or board[y + 1][x - 1] != "   "):
        print("Cant move down left!")
        return move(player, x)
    
    done = 1
    while(done == 1):
        y = y + 1
        x = x - 1
        if (y > 4 or x < 0):
            done = 0
        elif (board[y][x] == "   "):
            continue
        else: done = 0
        
    y = y - 1
    x = x + 1
    print(x)
    print(y)
    return x,y
    
def replace(coords, player, startCoordinates):
    if (coords == 0):
        return replaceUp(player, startCoordinates)
    elif (coords == 1):
        return replaceDown(player, startCoordinates)
    elif (coords == 2):
        return replaceRight(player, startCoordinates)
    elif (coords == 3):
        return replaceLeft(player, startCoordinates)
    elif (coords == 4):
        return replaceUpRight(player, startCoordinates)
    elif (coords == 5):
        return replaceUpLeft(player, startCoordinates)
    elif (coords == 6):
        return replaceDownRight(player, startCoordinates)
    elif (coords == 7):
        return replaceDownLeft(player, startCoordinates)
    
def move(player, startCoordinates):
    print("""In what direction would you like to move that piece?
           0 = UP
           1 = DOWN
           2 = RIGHT
           3 = LEFT
           4 = UP-RIGHT
           5 = UP-LEFT
           6 = DOWN-RIGHT
           7 = DOWN-LEFT
           """)
    target = input("Direction:")
    if (target.isdigit()):
        if (int(target) >= 0 and int(target) <= 7):
            return replace(int(target), player, startCoordinates)
            
def updateBoard(player, finalCoords, startCoordinates):
    x = finalCoords[0]
    y = finalCoords[1]
    if (player == 1):
        board[y][x] = " X "
    else : board[y][x] = " O "
    
    x = int(startCoordinates[0])
    y = int(startCoordinates[1])
    board[y][x] = empty
    
    return

def turn(player):
    possible = getPiecesCoordinates(player)
    print("Enter the coordinates of the piece you wish to move in the format: xy")
    piece = input("Coordinates:")
    
    if (len(piece) != 2 or piece[0] not in letters or piece[1].isdigit() == False):
        print("Invalid Coordinates. Try again\n")
        return turn(player)
    
    startCoordinates = str(letters[piece[0]] * 10 + int(piece[1]) - 1).zfill(2);
    
    if (startCoordinates not in possible):
        print("That square does not contain a valid piece. Try again\n")
        return turn(player)
    
    finalCoords = move(player, startCoordinates)
    
    updateBoard(player, finalCoords, startCoordinates)
    
    return
    
def checkPieces(list):
    pieces = [int(list[0]), int(list[1]), int(list[2])]
    
    if (pieces[0] + 10 == pieces[1] and pieces[1] + 10 == pieces[2]):
        return True;
    if (pieces[0] + 1 == pieces[1] and pieces[1] + 1 == pieces[2]):
        return True;    
    if (pieces[0] + 11 == pieces[1] and pieces[1] + 11 == pieces[2]):
        return True;    
    if (pieces[0] - 9 == pieces[2] and pieces[1] - 9 == pieces[2]):
        return True;
    
    return False;

def checkWin():
    player1Pieces = getPiecesCoordinates(1)
    player2Pieces = getPiecesCoordinates(2)
    
    if (checkPieces(player1Pieces)):
        print("Player 1 Wins!")
        return True;
    elif (checkPieces(player2Pieces)):
        print("Player 2 Wins!")
        return True;
    
    return False;   

def pvp():
    drawBoard()
    player = 1
    done = 1
    while(done == 1):
        if (player == 1):
            print("Player 1 Turn\n")
            turn(1)
        else:
            print("Player 2 Turn\n")
            turn(2)
        player = 1 + (player % 2)
        drawBoard()
        if (checkWin()):
            return

def main():
    gameMode = draw_menu()
    if (gameMode == 1):
        return pvp()
    
    
main()