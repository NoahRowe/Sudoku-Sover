import numpy as np
import pygame as pg
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

    # SOLVE IS TURNED INTO A STEP TOWARDS SOLVING THE BOARD  - THIS FUNCTION GETS ITTERATED
    def solve(self):
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

            # NEED TO EXIT THE WHILE LOOP AND GO AGAIN
            return

        print("Solved: ", self.isSolved())
        self.display()

    def checkSolvedBefore(self, row, col):
        for r in range(SIZE):
            for c in range(SIZE):

                if r == row and c == col:
                    return True

                if not self.cells[r, c].solved:
                    return False

    def setStartVals(self):

        for r in range(SIZE):
            for c in range(SIZE):
                self.cells[r, c].num = 0

        self.cells[0, 0].num = 5
        self.cells[0, 1].num = 3
        self.cells[0, 4].num = 7
        self.cells[1, 0].num = 6
        self.cells[1, 3].num = 1
        self.cells[1, 4].num = 9
        self.cells[1, 5].num = 5
        self.cells[2, 1].num = 9
        self.cells[2, 2].num = 8
        self.cells[2, 7].num = 6
        self.cells[3, 0].num = 8
        self.cells[3, 4].num = 6
        self.cells[3, 8].num = 3
        self.cells[4, 0].num = 4
        self.cells[4, 3].num = 8
        self.cells[4, 5].num = 3
        self.cells[4, 8].num = 1
        self.cells[5, 0].num = 7
        self.cells[5, 4].num = 2
        self.cells[5, 8].num = 6
        self.cells[6, 1].num = 6
        self.cells[6, 6].num = 2
        self.cells[6, 7].num = 8
        self.cells[7, 3].num = 4
        self.cells[7, 4].num = 1
        self.cells[7, 5].num = 9
        self.cells[7, 8].num = 5
        self.cells[8, 4].num = 8
        self.cells[8, 7].num = 7
        self.cells[8, 8].num = 9

        for r in range(SIZE):
            for c in range(SIZE):
                if self.cells[r, c].num != 0:
                    self.cells[r, c].solved = True

    def display(self):
        print("- " * (SIZE + 1))

        for r in range(SIZE):

            if r % 3 == 0 and r != 0:
                print("- " * (SIZE + 1))
            print("| ", end="")

            for c in range(SIZE):
                if c % 3 == 0 and c != 0:
                    print(" | ", end="")
                print(self.cells[r, c].num, end="")
            print(" |")

        print("- " * (SIZE + 1))

    def isSolved(self):
        for r in range(SIZE):
            for c in range(SIZE):
                if self.cells[r, c].num == 0:
                    return False
        return True

    def getStartBoard(self):
        board = []
        for r in range(SIZE):
            temp = []
            for c in range(SIZE):
                temp.append(self.cells[r, c].num)
            board.append(temp)
        return board

    def drawBoard(self, win, dSize):
        font = pg.font.SysFont("comicsans", 70)
        voffset = 15
        hoffset = 27
        gap = dSize / 9
        x = SIZE * gap
        y = SIZE * gap

        for r in range(SIZE):
            for c in range(SIZE):
                if self.cells[r, c].num == 0:
                    colour = WHITE
                else:
                    colour = BLACK

                text = font.render(str(self.cells[r, c].num), 1, colour)
                win.blit(text, (gap * c + hoffset, gap * r + voffset))






def genListOfIndex():
    temp = []
    for r in range(SIZE):
        for c in range(SIZE):
            temp.append([r, c])

    return np.array(temp)

def drawGrid(win, dSize):
    # Draw Grid Lines
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
    # p.display()
    # p.solve()

    disWidth = 700
    disHeight = 700
    dSize = disWidth

    cellW = 50
    cellH = 50
    cellS = 10

    win = pg.display.set_mode((disWidth, disHeight))
    pg.display.set_caption("Sudoku")
    clock = pg.time.Clock()

    crashed = False

    while not crashed:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                crashed = True

        win.fill(WHITE)
        if not p.isSolved():
            p.solve()
        p.drawBoard(win, dSize)
        drawGrid(win, dSize)
        clock.tick(120)

        pg.display.flip()


main()
