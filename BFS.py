import os
import sys
from abc import ABC, abstractmethod

# Helper functions to aid in your implementation. Can edit/remove
def toInt(c):
    return ord(c) - 97

def check(move):
    return toInt(move[0]) >= 0 & toInt(move[0]) < 26 & move[1] >= 0

class Piece(ABC):
    def __init__(self, move):
        self.x = toInt(move[0])
        self.y = move[1]

    @abstractmethod
    def validMove(self, nextMove):
        pass

    def __str__(self):
        return '(' + chr(self.x + 97) + ', ' + str(self.y) + ')'

class King(Piece):
    def validMove(self, nextMove):
        return abs(toInt(nextMove[0]) - self.x) <= 1 and abs(nextMove[1] - self.y) <= 1

class Rook(Piece):
    def validMove(self, nextMove):
        return (toInt(nextMove[0]) == self.x) or (nextMove[1] == self.y)

class Bishop(Piece):
    def validMove(self, nextMove):
        return abs(toInt(nextMove[0]) - self.x) == abs(nextMove[1] - self.y)

class Queen(Piece):
    def validMove(self, nextMove):
        return (toInt(nextMove[0]) == self.x) or (nextMove[1] == self.y) or (abs(toInt(nextMove[0]) - self.x) == abs(nextMove[1] - self.y))

class Knight(Piece):
    def validMove(self, nextMove):
        return (toInt(nextMove[0]) - self.x + nextMove[1] - self.y) == 3 and (toInt(nextMove[0]) > 0) and (nextMove[1] > 0)

class Obstacle(Piece):
    def validMove(self, nextMove):
        return false

class Board:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.table = []
        for i in range(length):
            currRow = []
            for j in range(width):
                currRow.append(0)
            self.table.append(currRow)

class State:
    pass

def search():
    pass


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_BFS():
    # You can code in here but you cannot remove this function or change the return type

    moves, nodesExplored = search() #For reference
    return moves, nodesExplored #Format to be returned

p1 = King(['a', 0])
print(p1)
print(p1.validMove(['b', 1]))
k1 = Rook(['c', 4])
print(k1)
print(k1.validMove(['d', 4]))