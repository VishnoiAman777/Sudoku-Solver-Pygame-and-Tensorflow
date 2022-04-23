def finalOutput(grid):
    print("")
    print("Solved Sudoku: ")
    print(" ")
    for row in range(9):
        for col in range(9):
            print(grid[row][col], end=" ")

        print()


def checkEnteredGrid(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] < 0 or grid[row][col] > 9:
                return False

    return True


def searchEmptyLocation(grid, loc):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                loc[0] = row
                loc[1] = col

                return True

    return False


def presentInRow(grid, row, num):
    for col in range(9):
        if grid[row][col] == num:
            return True

    return False


def presentInColumn(grid, col, num):
    for row in range(9):
        if grid[row][col] == num:
            return True

    return False


def presentIn3x3Box(grid, r, c, num):
    for row in range(3):
        for col in range(3):
            if grid[row + r][col + c] == num:
                return True

    return False


def checkLocation(grid, row, col, num):
    return not presentInRow(grid, row, num) and not presentInColumn(grid, col, num) and not presentIn3x3Box(grid,
                                                                                                            row - row % 3,
                                                                                                            col - col % 3,
                                                                                                            num)


def solveSudoku(grid):
    loc = [0, 0]

    if not searchEmptyLocation(grid, loc):
        return True

    row = loc[0]
    col = loc[1]

    for num in range(1, 10):
        if checkLocation(grid, row, col, num):
            grid[row][col] = num

            if solveSudoku(grid):
                return True

            grid[row][col] = 0

    return False


if __name__ == "__main__":

    print("Please enter your sudoku grid (use 0 for denoting empty space): ")
    print(" ")

    grid = [[int(i) for i in input().split()] for y in range(9)]

    if checkEnteredGrid(grid):
        if solveSudoku(grid):
            finalOutput(grid)
        else:
            print("")
            print("No Solution!")
    else:
        print("")
        print("Please enter proper numbers!")
