import os
import sys
from enum import Enum

# Helper functions to aid in your implementation. Can edit/remove
def toInt(c):
    return ord(c) - 97

def toChar(i):
    return chr(i + 97)

def check(move):
    return toInt(move[0]) >= 0 & toInt(move[0]) < 26 & move[1] >= 0

def clean(s):
    s = s.replace('[', '')
    s = s.replace(']', '')
    return s

def isStepCost(step):
    if not step.startswith('[') and not step.endswith(']'):
        return False
    step = clean(step)
    arr = step.split(',')
    try:
        int(arr[1])
        return True
    except Exception as err:
        return False

def isPiece(piece):
    if not piece.startswith('[') and not piece.endswith(']'):
        return False
    piece = clean(piece)
    arr = piece.split(',')
    try:
        Type[arr[0]]
        return True
    except Exception as err:
        return False
    
# Type of chess piece
class Type(Enum):
    King = 'King'
    Rook = 'Rook'
    Bishop = 'Bishop'
    Queen = 'Queen'
    Knight = 'Knight'
    Obstacle = 'Obstacle'

# Position of chess piece - x is char and y is int
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return '(' + self.x + ',' + str(self.y) + ')'

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return (self.x == other.x) and (self.y == other.y)
    
    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

# Representation of a chess piece - its current Position and its Type
class Piece:
    def __init__(self, pos, type):
        self.x = toInt(pos.x)
        self.y = pos.y
        self.type = type

    def validMove(self, nextMove):
        if self.type == Type.King:
            return abs(toInt(nextMove.x) - self.x) <= 1 and abs(nextMove.y - self.y) <= 1
        elif self.type == Type.Rook:
            return (toInt(nextMove.x) == self.x) or (nextMove.y == self.y)
        elif self.type == Type.Bishop:
            return abs(toInt(nextMove.x) - self.x) == abs(nextMove.y - self.y)
        elif self.type == Type.Queen:
            return (toInt(nextMove.x) == self.x) or (nextMove.y == self.y) or (abs(toInt(nextMove.x) - self.x) == abs(nextMove.y - self.y))
        elif self.type == Type.Knight:
            return (toInt(nextMove.x) - self.x + nextMove.y - self.y) == 3 and (toInt(nextMove.x) > 0) and (nextMove.y > 0)
        else:
            return False

    def validMoves(self, board):
        xs = []
        height = board.height
        width = board.width
        if self.type == Type.King:
            return abs(toInt(nextMove.x) - self.x) <= 1 and abs(nextMove.y - self.y) <= 1
        elif self.type == Type.Rook:
            return (toInt(nextMove.x) == self.x) or (nextMove.y == self.y)
        elif self.type == Type.Bishop:
            return abs(toInt(nextMove.x) - self.x) == abs(nextMove.y - self.y)
        elif self.type == Type.Queen:
            return (toInt(nextMove.x) == self.x) or (nextMove.y == self.y) or (abs(toInt(nextMove.x) - self.x) == abs(nextMove.y - self.y))
        elif self.type == Type.Knight:
            return (toInt(nextMove.x) - self.x + nextMove.y - self.y) == 3 and (toInt(nextMove.x) > 0) and (nextMove.y > 0)
        return xs
    
    def threateningMoves(self, board):
        xs = []
        height = board.height
        width = board.width
        for i in range(board.height + 1):
            for j in range(board.width + 1):
                curr = Position(toChar(i), j)
                if curr == self.getPosition():
                    continue
                if self.validMove(curr):
                    xs.append(curr)
        return xs

    def getPosition(self):
        return Position(toChar(self.x), self.y)

    def setPosition(self, pos):
        self.x = toInt(pos.x)
        self.y = pos.y 

    def __str__(self):
        return self.type.name + ' at ' + '(' + toChar(self.x) + ',' + str(self.y) + ')'

# Representation of a chess board - including height and width
class Board:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.table = []
        for i in range(height + 1):
            currRow = []
            for j in range(width + 1):
                currRow.append(1)
            self.table.append(currRow)
    
    def __str__(self):
        res = ""
        for row in self.table:
            res = res + str(row) + "\n"
        return res

# Representation of the state of the chess game
class State:
    def __init__(self, filepath):
        # table: store hash value of pieces, board: store access cost,
        # piece: store starting position, goal: store goal
        isEnemy = False
        isAlly = False
        self.table = {}
        count = 1
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                # Get the number of rows
                if line.startswith("Rows"):
                    boardRow = int(line.split("Rows:")[1])

                # Get the number of column and initiate chess board
                elif line.startswith("Cols"):
                    boardCol = int(line.split("Cols:")[1])
                    self.board = Board(boardRow, boardCol)

                # Get and add all obstacle to the chess table
                elif line.startswith("Position of Obstacles"):
                    line = line.split("Position of Obstacles (space between):")[1]
                    obstacles = line.split(" ")
                    for obstacle in obstacles:
                        pos = Position(obstacle[0], int(obstacle[1:]))
                        curr = Piece(pos, Type.Obstacle)
                        self.table[pos] = curr

                # Get and add all step cost to each position of the chess table
                elif isStepCost(line):
                    line = clean(line)
                    arr = line.split(',')
                    self.board.table[toInt(arr[0][0])][int(arr[0][1:])] = int(arr[1])

                elif line.startswith('Number of Enemy King, Queen'):
                    isEnemy = True
                elif line.startswith('Number of Own King, Queen, Bishop'):
                    isAlly = True
                    isEnemy = False

                # Get and add enemy piece and threatening positions (added as obstacle)
                elif isEnemy and isPiece(line):
                    line = clean(line)
                    arr = line.split(',')
                    pos = Position(arr[1][0], int(arr[1][1:]))
                    curr = Piece(pos, Type[arr[0]])
                    self.table[pos] = curr
                    xs = curr.threateningMoves(self.board)
                    for value in xs:
                        if value not in self.table:
                            self.table[value] = Piece(value, Type.Obstacle)

                # Get and add the starting piece of the game
                elif isAlly and isPiece(line):
                    line = clean(line)
                    arr = line.split(',')
                    pos = Position(arr[1][0], int(arr[1][1:]))
                    curr = Piece(pos, Type[arr[0]])
                    self.piece = curr

                # Get the goal position
                elif line.startswith('Goal Positions'):
                    line = line.split('Goal Positions (space between):')[1]
                    self.goal = Position(line[0], int(line[1:]))

                line = fp.readline()
                count = count + 1


def search():
    pass


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_UCS():
    # You can code in here but you cannot remove this function or change the return type

    moves, nodesExplored, pathCost= search() #For reference
    return moves, nodesExplored, pathCost #Format to be returned
    