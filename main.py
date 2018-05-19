import curses
import time
import sys
from curses import wrapper
from ms_objects import MineField
from ui import UI
from match import Match

class Game:

    def __init__(self, screen):
        self.screen = screen
        self.screen.refresh()
        self.ui = UI(screen)

    def play(self, w, h, m):

        m = Match(self.ui, w, h, m)
        m.play()


def revealTest(mf,ui):
    ptr = (0,0)
    ui.newBoard(mf)
    ui.drawEntireBoard()
    ui.setMinePointer(ptr)
    while True:
        playerInput = ui.getInput()
        curses.beep()
        if playerInput == curses.KEY_RIGHT:
            newPtr = (ptr[0] + 1, ptr[1])
            if newPtr[0] < mf.x:
                ptr = newPtr
                ui.setMinePointer(ptr)
        elif playerInput == curses.KEY_LEFT:
            newPtr = (ptr[0] - 1, ptr[1])
            if newPtr[0] >= 0:
                ptr = newPtr
                ui.setMinePointer(ptr)

def main2(stdscreen):
    ui = UI(stdscreen)
    mf = MineField(20, 20, 50)
    #revealTest(mf,ui)

    ui.newBoard(mf)
    ui.drawEntireBoard()
    time.sleep(1)
    ui.setMinePointer((0,0))
    time.sleep(1)
    ui.setMinePointer((0,1))
    time.sleep(1)


    mf.reveal(2,2)
    ui.updateCell(2,2,False)
    time.sleep(2)
    mf.revealAll()
    ui.drawEntireBoard()
    time.sleep(2)
    ui.setMinePointer((1,2))
    time.sleep(1)
    playerInput = ui.getInput()


def main(stdscreen, w, h, m):
    g = Game(stdscreen)
    g.play(w, h, m)


if __name__ == '__main__':
    sys.setrecursionlimit(3000)
    if 1 < len(sys.argv) <= 4:
        width = 0
        height = 0
        mines = 0
        try:
            width = int(sys.argv[1])
            height = int(sys.argv[2])
            mines = int(sys.argv[3])
        except (IndexError, ValueError):
            print('USAGE: main.py <width> <height> <number_of_mines>')
            exit()
        wrapper(main, width, height, mines)
    else:
        print('USAGE: main.py <width> <height> <number_of_mines>')
    #mf = MineField(10,10,20)
    #mf.draw()
