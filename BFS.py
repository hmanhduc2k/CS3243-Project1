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

def isStepCost(step):
    if not step.startswith('[') and not step.endswith(']'):
        return False
    step = step.replace('[', '')
    step = step.replace(']', '')
    arr = step.split(',')
    try:
        int(arr[1])
        return True
    except Exception as err:
        return False

def isPiece(piece):
    if not piece.startswith('[') and not piece.endswith(']'):
        return False
    piece = piece.replace('[', '')
    piece = piece.replace(']', '')
    arr = piece.split(',')
    try:
        Type[arr[0]]
        return True
    except Exception as err:
        return False
    
class Type(Enum):
    King = 'King'
    Rook = 'Rook'
    Bishop = 'Bishop'
    Queen = 'Queen'
    Knight = 'Knight'
    Obstacle = 'Obstacle'

class Piece():
    def __init__(self, pos, type):
        self.x = toInt(pos[0])
        self.y = pos[1]
        self.type = type

    def validMove(self, nextMove):
        if type is Type.King:
            return abs(toInt(nextMove[0]) - self.x) <= 1 and abs(nextMove[1] - self.y) <= 1
        elif type is Type.Rook:
            return (toInt(nextMove[0]) == self.x) or (nextMove[1] == self.y)
        elif type is Type.Bishop:
            return abs(toInt(nextMove[0]) - self.x) == abs(nextMove[1] - self.y)
        elif type is Type.Queen:
            return (toInt(nextMove[0]) == self.x) or (nextMove[1] == self.y) or (abs(toInt(nextMove[0]) - self.x) == abs(nextMove[1] - self.y))
        elif type is Type.Knight:
            return (toInt(nextMove[0]) - self.x + nextMove[1] - self.y) == 3 and (toInt(nextMove[0]) > 0) and (nextMove[1] > 0)
        else:
            return False

    def position(self):
        return [toChar[self.x], self.y]

class Board:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.table = []
        for i in range(height):
            currRow = []
            for j in range(width):
                currRow.append(1)
            self.table.append(currRow)
    
    def __str__(self):
        res = ""
        for row in self.table:
            res = res + str(row) + "\n"
        return res


class State:
    def __init__(self, filepath):
        isEnemy = False
        isAlly = False
        self.table = {}
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                if line.startswith("Rows"):
                    boardRow = int(line.split("Rows:")[1])
                elif line.startswith("Cols"):
                    boardCol = int(line.split("Cols:")[1])
                    self.board = Board(boardRow, boardCol)
                elif line.startswith("Position of Obstacles"):
                    line = line.split("Position of Obstacles (space between):")[1]
                    obstacles = line.split(" ")
                    for obstacle in obstacles:
                        curr = Piece([obstacle[0], int(obstacle[1])], Type.Obstacle)
                        self.table[curr] = [obstacle[0], int(obstacle[1])]
                elif isStepCost(line):
                    line = line.strip()
                    line = line.replace('[', '')
                    line = line.replace(']', '')
                    arr = line.split(',')
                    self.board.table[toInt(arr[0][0])][int(arr[0][1])] = int(arr[1])
                elif line.startswith('Number of Enemy King, Queen, Bishop, '):
                    isEnemy = True
                elif line.startswith('Number of Own King, Queen, Bishop'):
                    isAlly = True
                    isEnemy = False 
                elif isEnemy and isPiece(line):
                    pass
                elif isAlly and isPiece(line):
                    pass
                elif line.startswith('Goal Positions'):
                    pass

                line = fp.readline()
            


def search():
    pass


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_BFS():
    # You can code in here but you cannot remove this function or change the return type

    moves, nodesExplored = search() #For reference
    return moves, nodesExplored #Format to be returned

# print(Board(21, 21))
filepath = sys.argv[1]
# print("Rows:21".split("Rows:"))
print(State(filepath).board)
print(State(filepath).table)