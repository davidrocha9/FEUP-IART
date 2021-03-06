# Neutreeko

Neutreeko is a 5x5 board game. There are two players: Black and White. The initial position of the pieces is fixed and given initially. Its objective is for the player to place his three pieces in a line, orthogonally or diagonally, with the three connected. The game starts from the player who controls the black pieces. The players, on their turn, move each of their pieces alternately. The piece runs through the cells, in a straight line, orthogonally or diagonally until it finds an occupied cell or the edge of the board. The game is said to be a draw if the same position occurs three times in a row.

## Prerequisites:

The game was developed using [Python](https://www.python.org) 3, which needs to be installed alongside some of its modules: 

- [Pygame](https://www.pygame.org/) 

```shell
pip install pygame

```
- [Pygame-menu](https://pygame-menu.readthedocs.io/en/4.0.1/#)

```shell
pip install pygame-menu

```

## Running the program:

You can run the programm in a Python IDE, or simply in the command line.

### In a Python IDE

- Just press run on the neutreeko.py file.

### In the command line:

- Always being in the project directory;

### For windows:

```shell
python game.py
```
### For linux:

```shell
python3 game.py
```

## In game:

![Main Screen](https://i.imgur.com/hLsAX8t.png)

1. Select one of the three available modes: Player vs Player, Player vs AI or AI vs AI.
2. In modes which use artificial intelligence there is an option to choose the desired algorithm (Minimax with or without Alpha-Beta cuts), difficulty (Simple, Advanced or Complex) and evaluation function(Simple or Complex).
3. To make a move just press the piece you want to move and the destination cell.
4. If you want to ask for a hint just press the "H" key.
5. Statistics are displayed every time an AI makes a move, which contains the amount of time taken for a specific move as well as the amount of nodes traversed.
