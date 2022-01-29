import os
import sys

# Helper functions to aid in your implementation. Can edit/remove
class Piece:
    pass

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
