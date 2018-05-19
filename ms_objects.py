import random
import curses

class Cell:

    def __init__(self, isMine, numMines=0):
        self.mine = isMine
        self.revealed = False
        self.flagged = False
        self.surrounding = numMines

class MineField:

    AROUND = ((-1,1),(-1,0),(-1,-1),(0,1),(0,-1),(1,1),(1,0),(1,-1))

    def __init__(self,x,y,mines):
        self.board = []
        self.x = x
        self.y = y
        self.mines = mines
        self.flagsRemaining = mines
        self.spacesLeft = (x*y) - mines
        if mines > x * y:
            raise ValueError("Mines Cannot Be Greater Than Board Size")
        self.new()

    def clear(self):
        self.board = []
        for i in range(self.y):
            self.board.append([None] * self.x)

    def draw(self):
        for y in range(self.y):
            for x in range(self.x):
                if self.board[y][x].mine:
                    print('\033[91m!\033[0m ', end='')
                else:
                    print(str(self.board[y][x].surrounding),end=' ')
            print()

    def getCell(self, ptr):
        return self.board[ptr[1]][ptr[0]]

    def getSurroundingCells(self, x, y):
        surrounding = []
        for tup in MineField.AROUND:
            newX = x + tup[0]
            newY = y + tup[1]
            if (newX >= 0 and newY >= 0) and (newX < self.x and newY < self.y):
                surrounding.append((newX,newY))
        return surrounding

    def new(self):
        self.clear()
        for i in range(self.mines):
            x = random.randrange(0,self.x)
            y = random.randrange(0, self.y)
            while self.board[y][x] is not None:
                x = random.randrange(0, self.x)
                y = random.randrange(0, self.y)
            self.board[y][x] = Cell(True)
        for y in range(self.y):
            for x in range(self.x):
                if self.board[y][x] is None:
                    surrounding = self.getSurroundingCells(x,y)
                    numMines = 0
                    for cor in surrounding:
                        if self.board[cor[1]][cor[0]] is not None and self.board[cor[1]][cor[0]].mine:
                            numMines += 1
                    self.board[y][x] = Cell(False,numMines)

    def reveal(self, ptr):
        cell = self.board[ptr[1]][ptr[0]]
        cell.revealed = True
        self.spacesLeft -= 1
        if cell.mine:
            return False
        if not cell.mine and cell.surrounding == 0:
            surrounding = self.getSurroundingCells(ptr[0],ptr[1])
            for cor in surrounding:
                if not self.getCell(cor).revealed:
                    self.reveal(cor)
        return True

    def flag(self, ptr):
        self.board[ptr[1]][ptr[0]].flagged = not self.board[ptr[1]][ptr[0]].flagged

    def revealAll(self):
        for y in range(self.y):
            for x in range(self.x):
                self.board[y][x].revealed = True

    def revealMines(self):
        for y in range(self.y):
            for x in range(self.x):
                if self.board[y][x].mine:
                    self.board[y][x].revealed = True
