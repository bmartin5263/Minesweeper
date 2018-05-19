import curses
import time
from ms_objects import MineField

class Match:

    MOVEMENT = (curses.KEY_DOWN, curses.KEY_UP, curses.KEY_LEFT, curses.KEY_RIGHT)

    def __init__(self, ui, width, height, mines):
        self.ui = ui
        self.minefield = MineField(width,height,mines)
        self.complete = False
        self.minePointer = (0,0)

    def flag(self):
        self.minefield.flag(self.minePointer)
        self.ui.updateCell(self.minePointer[0], self.minePointer[1], True)

    def movePointer(self, movement):
        originalLocation = tuple(self.minePointer)
        if movement == curses.KEY_RIGHT:
            self.minePointer = (self.minePointer[0] + 1, self.minePointer[1])
            if self.minePointer == originalLocation:
                return False

            if not self.minePointer[0] < self.minefield.x:
                self.minePointer = (0, self.minePointer[1] + 1)
                if self.minePointer == originalLocation:
                    return False
                if not self.minePointer[1] < self.minefield.y:
                    self.minePointer = (0, 0)
                    if self.minePointer == originalLocation:
                        return False
            while self.minefield.getCell(self.minePointer).revealed:
                self.minePointer = (self.minePointer[0] + 1, self.minePointer[1])
                if self.minePointer == originalLocation:
                    return False
                if not self.minePointer[0] < self.minefield.x:
                    self.minePointer = (0, self.minePointer[1]+1)
                    if self.minePointer == originalLocation:
                        return False
                    if not self.minePointer[1] < self.minefield.y:
                        self.minePointer = (0,0)
                        if self.minePointer == originalLocation:
                            return False

        elif movement == curses.KEY_LEFT:
            self.minePointer = (self.minePointer[0] - 1, self.minePointer[1])
            if self.minePointer == originalLocation:
                return False

            if not self.minePointer[0] >= 0:
                self.minePointer = (self.minefield.x-1, self.minePointer[1] - 1)
                if self.minePointer == originalLocation:
                    return False
                if not self.minePointer[1] >= 0:
                    self.minePointer = (self.minefield.x - 1, self.minefield.y - 1)
                    if self.minePointer == originalLocation:
                        return False
            while self.minefield.getCell(self.minePointer).revealed:
                self.minePointer = (self.minePointer[0] - 1, self.minePointer[1])
                if self.minePointer == originalLocation:
                    return False
                if not self.minePointer[0] >= 0:
                    self.minePointer = (self.minefield.x - 1, self.minePointer[1] - 1)
                    if self.minePointer == originalLocation:
                        return False
                    if not self.minePointer[1] >= 0:
                        self.minePointer = (self.minefield.x - 1, self.minefield.y - 1)
                        if self.minePointer == originalLocation:
                            return False

        elif movement == curses.KEY_DOWN:
            self.minePointer = (self.minePointer[0], self.minePointer[1] + 1)
            if self.minePointer == originalLocation:
                return False

            if not self.minePointer[1] < self.minefield.y:
                self.minePointer = (self.minePointer[0]+1, 0)
                if self.minePointer == originalLocation:
                    return False
                if not self.minePointer[0] < self.minefield.x:
                    self.minePointer = (0, 0)
                    if self.minePointer == originalLocation:
                        return False
            while self.minefield.getCell(self.minePointer).revealed:
                self.minePointer = (self.minePointer[0], self.minePointer[1] + 1)
                if self.minePointer == originalLocation:
                    return False
                if not self.minePointer[1] < self.minefield.y:
                    self.minePointer = (self.minePointer[0] + 1, 0)
                    if self.minePointer == originalLocation:
                        return False
                    if not self.minePointer[0] < self.minefield.x:
                        self.minePointer = (0, 0)
                        if self.minePointer == originalLocation:
                            return False

        elif movement == curses.KEY_UP:
            self.minePointer = (self.minePointer[0], self.minePointer[1] - 1)
            if self.minePointer == originalLocation:
                return False

            if not self.minePointer[1] >= 0:
                self.minePointer = (self.minePointer[0] - 1, self.minefield.y - 1)
                if self.minePointer == originalLocation:
                    return False
                if not self.minePointer[0] >= 0:
                    self.minePointer = (self.minefield.x - 1, self.minefield.y - 1)
                    if self.minePointer == originalLocation:
                        return False
            while self.minefield.getCell(self.minePointer).revealed:
                self.minePointer = (self.minePointer[0], self.minePointer[1] - 1)
                if self.minePointer == originalLocation:
                    return False
                if not self.minePointer[1] >= 0:
                    self.minePointer = (self.minePointer[0] - 1, self.minefield.y - 1)
                    if self.minePointer == originalLocation:
                        return False
                    if not self.minePointer[0] >= 0:
                        self.minePointer = (self.minefield.x - 1, self.minefield.y - 1)
                        if self.minePointer == originalLocation:
                            return False

        self.ui.setMinePointer(self.minePointer)
        return True

    def play(self):
        self.ui.newBoard(self.minefield)
        self.ui.drawEntireBoard()
        self.ui.setMinePointer(self.minePointer)
        while not self.complete and self.minefield.spacesLeft > 0:
            playerInput = self.ui.getInput()
            if playerInput in Match.MOVEMENT:
                self.movePointer(playerInput)
            elif playerInput == ord(' '):
                self.reveal()
            elif playerInput == ord('f'):
                self.flag()

    def reveal(self):
        safe = self.minefield.reveal(self.minePointer)
        if not safe:
            self.minefield.revealMines()
            self.ui.drawEntireBoard()
            self.complete = True
            curses.beep()
            time.sleep(5)
        else:
            self.ui.drawEntireBoard()
            if self.minefield.spacesLeft == 0:
                curses.beep()
                self.complete = True