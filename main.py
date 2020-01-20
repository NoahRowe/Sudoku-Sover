import numpy as np
import pygame as pg

from initPuzzle import initStartVals

pg.font.init()

SIZE = 9
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Cell:

    def __init__(self, row, col, n):
        self.num = n
        self.row = row
        self.col = col
        self.grid = int(col/3) + int(row/3)*3
        self.solved = False


class Puzzle:

    def __init__(self):
        self.cells = []
        self.solved = False
        self.index = 0

        # init vals at 0
        for r in range(SIZE):
            temp = []
            for c in range(SIZE):
                val = Cell(r, c, 0)
                val.num = 0
                temp.append(val)

            self.cells.append(temp)

        self.cells = np.array(self.cells)

    def getGridVals(self, row, col):
        # Gets the mini 3x3 values used to determine options for a specific cell - called in getOptions
        gridVals = np.array([])
        for r in range(3):  # Row vals
            for c in range(3):  # Col vals
                rIndex = (row // 3) * 3 + r
                cIndex = (col // 3) * 3 + c
                if rIndex == row and cIndex == col:
                    pass
                else:
                    gridVals = np.append(gridVals, self.cells[rIndex, cIndex].num)

        return gridVals

    def getOptions(self, row, col):
        # Gets the allowed values for a single cell - could be optimized
        options = np.arange(1, 10)
        puzRow = []
        puzCol = []
        puzGrid = self.getGridVals(row, col)
        for i in range(SIZE):
            if i != col:
                puzRow.append(self.cells[row, i].num)
            if i != row:
                puzCol.append(self.cells[i, col].num)

        nonOptions = np.unique(np.concatenate((puzRow, puzCol, puzGrid), axis=None))
        nonOptions = list(nonOptions)
        if 0 in nonOptions:
            nonOptions.remove(0)

        nonOptions = np.array(nonOptions)

        # These are the possible values that can be in this cell
        possVals = np.setxor1d(options, nonOptions)
        possVals = possVals.astype(int)

        return possVals

    def solve(self):
        # Solve function that is currently only one iteration towards a full solution - change index and return to fix
        # index = 0
        listToIndex = genListOfIndex()

        while self.index < SIZE**2:
            if self.index < 0:
                print("Did not find solution")
                return

            noOptions = False
            r, c = listToIndex[self.index]
            if self.cells[r, c].solved:
                self.index += 1
                return
                # continue

            possVals = self.getOptions(r, c)

            if len(possVals > 0):
                if self.cells[r, c].num == 0:  # unset, will guess the lowest permutation

                    self.cells[r, c].num = possVals[0]

                    # Checks if value is certainly right
                    if len(possVals) == 1 and self.checkSolvedBefore(r, c):
                        self.cells[r, c].solved = True
                    else:
                        self.cells[r, c].solved = False

                    self.index += 1

                else: # Has been previously set, need to try a new option
                    # make sure that the current number is in the options list
                    possVals = list(set(np.append(possVals, self.cells[r, c].num)))
                    possVals = np.sort(possVals)
                    # Find the next highest value in the list
                    i = np.where(possVals == self.cells[r, c].num)[0][0]
                    if i+1 == len(possVals):  # No more options left to try - Need to backtrack again
                        noOptions = True
                    else:
                        self.cells[r, c].num = possVals[i+1]  # Next highest val
                        self.index += 1

            if len(possVals) == 0 or noOptions:  # Need to go to the last option that we tried
                self.cells[r, c].num = 0
                self.cells[r, c].solved = False
                self.index -= 1
                r, c = listToIndex[self.index]
                # Itterate to find the last cell that we can change
                while self.cells[r, c].solved:
                    self.index -= 1
                    r, c = listToIndex[self.index]

            # Remove this return to solve in one iteration
            return

    def checkSolvedBefore(self, row, col):
        # Checks to see if any values before cell[row, col] are not solved for sure yet
        for r in range(SIZE):
            for c in range(SIZE):

                if r == row and c == col:
                    return True

                if not self.cells[r, c].solved:
                    return False

    def setStartVals(self):
        # Uses initPuzzle.py to set the static values of the board
        board = initStartVals()

        for r in range(SIZE):
            for c in range(SIZE):
                self.cells[r, c].num = board[r, c]

                if self.cells[r, c].num != 0:
                    self.cells[r, c].solved = True

    def isSolved(self):
        # Check if the board is solved
        for r in range(SIZE):
            for c in range(SIZE):
                if self.cells[r, c].num == 0:
                    return False
        return True

    def drawBoard(self, win, dSize):
        # Function to draw the board values to the win
        font = pg.font.SysFont("comicsans", 70)
        voffset = 15
        hoffset = 27
        gap = dSize / 9
        x = SIZE * gap
        y = SIZE * gap

        for r in range(SIZE):
            for c in range(SIZE):
                # Do not display unsolved values
                if self.cells[r, c].num == 0:
                    colour = WHITE
                else:
                    colour = BLACK

                text = font.render(str(self.cells[r, c].num), 1, colour)
                win.blit(text, (gap * c + hoffset, gap * r + voffset))


class Button:

    def __init__(self, x, y, w, h, text, c):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.colour = c

    def draw(self, win):
        # Draw a black boarder and then the button box
        pg.draw.rect(win, (0, 0, 0), (self.x-2, self.y-2, self.w+4, self.h+4), 0)
        pg.draw.rect(win, self.colour, (self.x, self.y, self.w, self.h), 0)

        # Put in the text
        fnt = pg.font.SysFont('comicsans', 50)
        text = fnt.render(self.text, 1, (0, 0, 0))
        win.blit(text, (self.x + (self.w/2 - text.get_width()/2), self.y + (self.h/2 - text.get_height()/2)))

    def onTop(self, mousePos):
        # Determine if the mouse is on top of the button
        x, y = mousePos
        if self.x < x < self.x + self.w:
            if self.y < y < self.y + self.h:
                return True
        return False

def genListOfIndex():
    # Generate a list of index values to iterate through a SIZExSIZE grid
    temp = []
    for r in range(SIZE):
        for c in range(SIZE):
            temp.append([r, c])

    return np.array(temp)


def drawGrid(win, dSize):
    # Draw Grid Lines to the window
    gap = dSize / 9
    for i in range(SIZE + 1):
        if i % 3 == 0 and i != 0:
            thick = 4
        else:
            thick = 1
        pg.draw.line(win, (0, 0, 0), (0, i * gap), (dSize, i * gap), thick)
        pg.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, dSize), thick)


def main():
    p = Puzzle()
    p.setStartVals()

    displayWidth = 700
    displayHeight = 700 + 80
    dSize = displayWidth

    win = pg.display.set_mode((displayWidth, displayHeight))
    pg.display.set_caption("Sudoku")
    clock = pg.time.Clock()

    sButtonW = 250
    sButtonH = 50
    sButtonX = (displayWidth - sButtonW) / 2
    sButtonY = displayHeight - sButtonH - 20

    startButton = Button(sButtonX, sButtonY, sButtonW, sButtonH, "Start Solution", (0, 200, 0))

    crashed = False
    startSolve = False

    while not crashed:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                crashed = True

            if event.type == pg.MOUSEBUTTONDOWN and not startSolve:
                mousePos = pg.mouse.get_pos()
                if startButton.onTop(mousePos):
                    startSolve = True

        win.fill(WHITE)
        if not p.isSolved() and startSolve:
            p.solve()
        p.drawBoard(win, dSize)
        drawGrid(win, dSize)
        startButton.draw(win)
        clock.tick(60)

        pg.display.flip()


main()
