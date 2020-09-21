backtracks = 0


def solveSudoku(grid, i=0, j=0):
    global backtracks
    i, j = findNextCellTOFill(grid)
    if i == -1:
        return True
    for e in range(1, 10):
        if isValid(grid, i, j, e):
            grid[i][j] = e
            if solveSudoku(grid, i, j):
                return True
            backtracks += 1
            grid[i][j] = 0
    return False


def findNextCellTOFill(grid):
    for x in range(0, 9):
        for y in range(0, 9):
            if grid[x][y] == 0:
                return x, y
    return -1, -1


def isValid(grid, i, j, e):
    rowOK = all([e != grid[i][x] for x in range(9)])
    if rowOK:
        clumnOK = all([e != grid[x][j] for x in range(9)])
        if clumnOK:
            secTopX, secTopY = 3*(i//3), 3*(j//3)
            for x in range(secTopX, secTopX + 3):
                for y in range(secTopY, secTopY + 3):
                    if grid[x][y] == e:
                        return False
            return True
    return False


def printSudoku(grid):
    numrow = 0
    for row in grid:
        if numrow % 3 == 0 and numrow != 0:
            print(' ')
        print(row[0:3], ' ', row[3:6], ' ', row[6:9])
        numrow += 1


if __name__ == '__main__':
    input_data = [[5, 1, 7, 6, 0, 0, 0, 3, 4],
                  [2, 8, 9, 0, 0, 4, 0, 0, 0],
                  [3, 4, 6, 2, 0, 5, 0, 9, 0],
                  [6, 0, 2, 0, 0, 0, 0, 1, 0],
                  [0, 3, 8, 0, 0, 6, 0, 4, 7],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 9, 0, 0, 0, 0, 0, 7, 8],
                  [7, 0, 3, 4, 0, 0, 5, 6, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    solveSudoku(input_data)
    printSudoku(input_data)
