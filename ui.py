import curses
import time

class UI:

    def __init__(self, screen):
        self.windows = {
            'main': {'window':screen, 'panel': None, 'location': None},
            'board': {'window': None, 'panel': None, 'location': None}
        }
        self.minefield = None
        self.minePointer = None

        curses.curs_set(0)
        curses.init_pair(1, 15, curses.COLOR_BLACK)
        curses.init_pair(2, 39, curses.COLOR_BLACK)
        curses.init_pair(3, 82, curses.COLOR_BLACK)
        curses.init_pair(4, 199, curses.COLOR_BLACK)
        curses.init_pair(5, 21, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(9, 11, curses.COLOR_BLACK)

        self.NUM_COLORS = {
            '1' : curses.color_pair(2), #blue
            '2' : curses.color_pair(3), #blue
            '3' : curses.color_pair(4), #blue
            '4' : curses.color_pair(5), #blue
            '5' : curses.color_pair(6), #blue
            '6' : curses.color_pair(7), #blue
            '7' : curses.color_pair(8), #blue
            '8' : curses.color_pair(9) #yellow

        }

    def newBoard(self, minefield):
        self.minefield = minefield
        window = curses.newwin(self.minefield.y + 2, (self.minefield.x * 2) + 1,  # height, length
                               0, 0)
        window.box()
        window.refresh()
        self.windows['board']['window'] = window

    def drawCell(self, x, y, hover):
        cell = self.minefield.board[y][x]
        if cell.revealed:
            if not cell.mine:
                surrounding = str(cell.surrounding)
                if surrounding != '0':
                    self.windows['board']['window'].addstr(y + 1, (x * 2) + 1, str(cell.surrounding), self.NUM_COLORS[surrounding])
                else:
                    self.windows['board']['window'].addstr(y + 1, (x * 2) + 1, ' ', curses.color_pair(2))

            else:
                self.windows['board']['window'].addstr(y + 1, (x * 2) + 1, 'X', curses.color_pair(9) | curses.A_BLINK)

        else:
            if hover:
                if cell.flagged:
                    self.windows['board']['window'].addstr(y + 1, (x * 2)+1, '☭', curses.color_pair(4))
                else:
                    self.windows['board']['window'].addstr(y + 1, (x * 2) + 1, '■', curses.color_pair(4))
            else:
                if cell.flagged:
                    self.windows['board']['window'].addstr(y + 1, (x * 2)+1, '☭', curses.color_pair(9))
                else:
                    self.windows['board']['window'].addstr(y + 1, (x * 2) + 1, '■', curses.color_pair(1))


    def drawEntireBoard(self):
        self.windows['board']['window'].box()
        for i in range(self.minefield.y):
            for j in range(self.minefield.x):
                try:
                    self.drawCell(j,i,False)
                except:
                    curses.beep()
        self.windows['board']['window'].refresh()

    def updateCell(self, x, y, hover):
        self.drawCell(x,y,hover)
        self.windows['board']['window'].refresh()

    def setMinePointer(self, ptr):
        if self.minePointer is not None:
            self.drawCell(self.minePointer[0],self.minePointer[1],False)
        self.minePointer = ptr
        if self.minePointer is not None:
            self.drawCell(self.minePointer[0], self.minePointer[1], True)
        self.windows['board']['window'].refresh()

    def getInput(self):
        curses.flushinp()
        k = self.windows['main']['window'].getch()
        return k