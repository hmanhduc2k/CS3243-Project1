import os
import sys
from enum import Enum
from collections import deque
from queue import PriorityQueue
import time

# Helper functions to aid in your implementation. Can edit/remove
def toInt(c):
    return ord(c) - 97

def toChar(i):
    return chr(i + 97)

def check(move):
    return toInt(move[0]) >= 0 & toInt(move[0]) < 26 & move[1] >= 0

def isValid(x, y, state):
    return (x >= 0) and (x < state.board.cols) and (y >= 0) and (y < state.board.rows) and (state.table.get(Position(toChar(x), y)) is None)

def isValidConstraint(x, y, board, table):
    return (x >= 0) and (x < board.cols) and (y >= 0) and (y < board.rows) and (table.get(Position(toChar(x), y)) is None or table.get(Position(toChar(x), y)).type is not Type.Obstacle)

def isObstacle(x, y, table):
    return table.get(Position(toChar(x), y)) is not None and table.get(Position(toChar(x), y)).type is Type.Obstacle

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
        self.x = x  # col number in character - horizontal value
        self.y = y  # row number in integer - vertical value
    
    def __str__(self):
        return '(' + self.x + ',' + str(self.y) + ')'
    
    def get(self):
        return self.x, self.y

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return (self.x == other.x) and (self.y == other.y)
    
    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

# Representation of a chess piece - its current Position and its Type
class Piece:
    def __init__(self, currentPosition, type):
        self.currentPosition = currentPosition
        self.previousPiece = None
        self.x = toInt(currentPosition.x)
        self.y = currentPosition.y
        self.type = type

    def __lt__(self, other):
        return isinstance(other, Piece) and self.x <= other.x

    def getKing(self, board, table):
        xs = []
        if isValidConstraint(self.x - 1, self.y - 1, board, table):
            xs.append(Position(toChar(self.x - 1), self.y - 1))
        if isValidConstraint(self.x - 1, self.y, board, table):
            xs.append(Position(toChar(self.x - 1), self.y))
        if isValidConstraint(self.x - 1, self.y + 1, board, table):
            xs.append(Position(toChar(self.x - 1), self.y + 1))
        if isValidConstraint(self.x, self.y - 1, board, table):
            xs.append(Position(toChar(self.x), self.y - 1))
        if isValidConstraint(self.x, self.y + 1, board, table):
            xs.append(Position(toChar(self.x), self.y + 1))
        if isValidConstraint(self.x + 1, self.y - 1, board, table):
            xs.append(Position(toChar(self.x + 1), self.y - 1))
        if isValidConstraint(self.x + 1, self.y, board, table):
            xs.append(Position(toChar(self.x + 1), self.y))
        if isValidConstraint(self.x + 1, self.y + 1, board, table):
            xs.append(Position(toChar(self.x + 1), self.y + 1))
        return xs

    def getKnight(self, board, table):
        xs = []
        if isValidConstraint(self.x - 2, self.y - 1, board, table):
            xs.append(Position(toChar(self.x - 2), self.y - 1))

        if isValidConstraint(self.x - 1, self.y - 2, board, table):
            xs.append(Position(toChar(self.x - 1), self.y - 2))

        if isValidConstraint(self.x + 2, self.y - 1, board, table):
            xs.append(Position(toChar(self.x + 2), self.y - 1))

        if isValidConstraint(self.x + 1, self.y - 2, board, table):
            xs.append(Position(toChar(self.x + 1), self.y - 2))

        if isValidConstraint(self.x - 2, self.y + 1, board, table):
            xs.append(Position(toChar(self.x - 2), self.y + 1))

        if isValidConstraint(self.x - 1, self.y + 2, board, table):
            xs.append(Position(toChar(self.x - 1), self.y + 2))

        if isValidConstraint(self.x + 1, self.y + 2, board, table):
            xs.append(Position(toChar(self.x + 1), self.y + 2))

        if isValidConstraint(self.x + 2, self.y + 1, board, table):
            xs.append(Position(toChar(self.x + 2), self.y + 1))
        return xs

    def getRook(self, board, table):
        xs = []
        temp = self.x
        while temp >= 0 and not isObstacle(temp, self.y, table):
            xs.append(Position(toChar(temp), self.y))
            temp = temp - 1
        temp = self.x
        while temp < board.cols and not isObstacle(temp, self.y, table):
            xs.append(Position(toChar(temp), self.y))
            temp = temp + 1
        temp = self.y
        while temp >= 0 and not isObstacle(self.x, temp, table):
            xs.append(Position(toChar(self.x), temp))
            temp = temp - 1
        temp = self.y
        while temp < board.rows and not isObstacle(self.x, temp, table):
            xs.append(Position(toChar(self.x), temp))
            temp = temp + 1
        return xs

    def getBishop(self, board, table):
        xs = []
        tempX = self.x
        tempY = self.y
        while tempX >= 0 and tempY >= 0 and not isObstacle(tempX, tempY, table):
            xs.append(Position(toChar(tempX), tempY))
            tempX = tempX - 1
            tempY = tempY - 1
        tempX = self.x
        tempY = self.y
        while tempX < board.cols and tempY >= 0 and not isObstacle(tempX, tempY, table):
            xs.append(Position(toChar(tempX), tempY))
            tempX = tempX + 1
            tempY = tempY - 1
        tempX = self.x
        tempY = self.y
        while tempX >= 0 and tempY < board.rows and not isObstacle(tempX, tempY, table):
            xs.append(Position(toChar(tempX), tempY))
            tempX = tempX - 1
            tempY = tempY + 1
        tempX = self.x
        tempY = self.y
        while tempX < board.cols and tempY < board.rows and not isObstacle(tempX, tempY, table):
            xs.append(Position(toChar(tempX), tempY))
            tempX = tempX + 1
            tempY = tempY + 1
        return xs

    def getPosition(self):
        return Position(toChar(self.x), self.y)

    def getThreateningConstraints(self, board, table):
        if self.type == Type.King:
            return self.getKing(board, table)
        elif self.type == Type.Rook:
            return self.getRook(board, table)
        elif self.type == Type.Bishop:
            return self.getBishop(board, table)
        elif self.type == Type.Queen:
            return self.getRook(board, table) + self.getBishop(board, table)
        elif self.type == Type.Knight:
            return self.getKnight(board, table)
        else:
            return []

    def getAdjacent(self, state):
        xs = []
        if isValid(self.x - 1, self.y - 1, state):
            xs.append(Position(toChar(self.x - 1), self.y - 1))
        if isValid(self.x - 1, self.y, state):
            xs.append(Position(toChar(self.x - 1), self.y))
        if isValid(self.x - 1, self.y + 1, state):
            xs.append(Position(toChar(self.x - 1), self.y + 1))
        if isValid(self.x, self.y - 1, state):
            xs.append(Position(toChar(self.x), self.y - 1))
        if isValid(self.x, self.y + 1, state):
            xs.append(Position(toChar(self.x), self.y + 1))
        if isValid(self.x + 1, self.y - 1, state):
            xs.append(Position(toChar(self.x + 1), self.y - 1))
        if isValid(self.x + 1, self.y, state):
            xs.append(Position(toChar(self.x + 1), self.y))
        if isValid(self.x + 1, self.y + 1, state):
            xs.append(Position(toChar(self.x + 1), self.y + 1))
        return xs

    def traceback(self):
        currentPiece = self
        xs = deque()
        while currentPiece.previousPiece is not None:
            curr = []
            curr.append(currentPiece.previousPiece.currentPosition.get())
            curr.append(currentPiece.currentPosition.get())
            xs.appendleft(curr)
            currentPiece = currentPiece.previousPiece
        return list(xs)

    def __str__(self):
        return self.type.name + ' at ' + '(' + toChar(self.x) + ',' + str(self.y) + ')'

    def rep(self):
        if self.type == Type.King:
            return 'K'
        elif self.type == Type.Rook:
            return 'R'
        elif self.type == Type.Bishop:
            return 'B'
        elif self.type == Type.Queen:
            return 'Q'
        elif self.type == Type.Knight:
            return 'M'
        else:
            return 'O'

# Representation of a chess board - including height and width
class Board:
    def __init__(self, rows, cols):
        self.rows = rows   # refers to the number of rows
        self.cols = cols   # refers to the number of columns
        self.table = []
        for i in range(rows):
            currRow = []
            for j in range(cols):
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
        self.goals = []
        self.obstacles = []
        self.enemies = []
        self.threats = {}
        count = 1
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                # Get the number of rows
                if line.startswith("Rows"):
                    self.boardRow = int(line.split("Rows:")[1])

                # Get the number of column and initiate chess board
                elif line.startswith("Cols"):
                    self.boardCol = int(line.split("Cols:")[1])
                    self.board = Board(self.boardRow, self.boardCol)

                # Get and add all obstacle to the chess table
                elif line.startswith("Position of Obstacles"):
                    line = line.split("Position of Obstacles (space between):")[1]
                    obstacles = line.split(" ")
                    if len(obstacles[0]) >= 2:
                        for obstacle in obstacles:
                            pos = Position(obstacle[0], int(obstacle[1:]))
                            curr = Piece(pos, Type.Obstacle)
                            self.table[pos] = curr
                            self.obstacles.append(pos)

                # Get and add all step cost to each position of the chess table
                elif isStepCost(line):
                    line = clean(line)
                    arr = line.split(',')
                    self.board.table[int(arr[0][1:])][toInt(arr[0][0])] = int(arr[1])

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
                    self.enemies.append(curr)
                    # xs = curr.threateningMoves(self.board)
                    xs = curr.getThreateningConstraints(self.board, self.table)
                    self.threats[curr] = xs
                    for value in xs:
                        if value not in self.table:
                            self.table[value] = Piece(value, Type[arr[0]])

                # Get and add the starting piece of the game
                elif isAlly and isPiece(line):
                    line = clean(line)
                    arr = line.split(',')
                    pos = Position(arr[1][0], int(arr[1][1:]))
                    curr = Piece(pos, Type[arr[0]])
                    self.piece = curr
                    self.table[pos] = curr

                # Get the goal position
                elif line.startswith('Goal Positions'):
                    line = line.split('Goal Positions (space between):')[1]
                    arr = line.split(' ')
                    for goal in arr:
                        self.goals.append(Position(goal[0], int(goal[1:])))

                line = fp.readline()
                count = count + 1

    def traceback(self, endPiece):
        currentPiece = endPiece
        xs = deque()
        self.table[currentPiece.currentPosition] = currentPiece
        while currentPiece.previousPiece is not None:
            curr = []
            curr.append(currentPiece.previousPiece.currentPosition.get())
            curr.append(currentPiece.currentPosition.get())
            xs.appendleft(curr)
            currentPiece = currentPiece.previousPiece
            self.table[currentPiece.currentPosition] = currentPiece
        return list(xs)

    def __str__(self):
        res = ''
        for i in range(self.board.rows):
            x = '|'
            if i < 10:
                x = '0' + str(i) + x
            else:
                x = str(i) + x
            for j in range(self.board.cols):
                curr = Position(toChar(j), i)
                if self.table.get(curr) is not None:
                    x = x + self.table.get(curr).rep() + '|'
                elif curr in self.goals:
                    x = x + 'G|'
                else:
                    x = x + ' |'
            x = x + '\n'
            res = res + x
        res = res + '  |'
        for j in range(self.board.cols):
            res = res + toChar(j) + '|'
        return res + '\n'
    
    def getInfo(self):
        print(str(self))
        print('Starting piece is ' + str(self.piece))
        print('Number of obstacles is ' + str(len(self.obstacles)))
        temp = 'Obstacles are in: '
        for pos in self.obstacles:
            temp = temp + str(pos) + ', '
        print(temp)
        print('Enemies are:')
        for piece in self.enemies:
            print(str(piece))
            a = 'Threatening positions: '
            for pos in self.threats.get(piece):
                a = a + str(pos) + ', '
            print(a)
        temp = 'Goal position(s): '
        for x in self.goals:
            temp = temp + str(x) + ', '
        print(temp + '\n')



def search():
    filepath = sys.argv[1]
    state = State(filepath)
    print(state)
    print(state.board)
    visited = {}
    q = PriorityQueue()

    moves = []
    nodesExplored = 0
    totalCost = 0

    count = state.board.table[state.piece.currentPosition.y][toInt(state.piece.currentPosition.x)]
    q.put((0, state.piece))

    while not q.empty():
        curr = q.get()
        cost = curr[0]
        node = curr[1]
        if visited.get(node.currentPosition) is not None:
            continue
        if node.currentPosition in state.goals:
            moves = state.traceback(node)
            totalCost = cost
            break
        for pos in node.getAdjacent(state):
            if visited.get(pos) is None:
                k = Piece(pos, Type.King)
                k.previousPiece = node
                q.put((cost + state.board.table[pos.y][toInt(pos.x)], k))
        visited[node.currentPosition] = True
        nodesExplored = nodesExplored + 1
    print(state)
    return moves, nodesExplored, totalCost

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_AStar():
    # You can code in here but you cannot remove this function or change the return type

    moves, nodesExplored, pathCost= search() #For reference
    return moves, nodesExplored, pathCost #Format to be returned
    