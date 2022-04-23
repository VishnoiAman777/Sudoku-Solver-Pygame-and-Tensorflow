import pygame
from sudoku_solver import *

pygame.font.init()
window = pygame.display.set_mode((500, 600))
pygame.display.set_caption("SUDOKU SOLVER USING BACKTRACKING ALGORITHM")
font = pygame.font.SysFont("timesnewroman", 30)
font1 = pygame.font.SysFont("timesnewroman", 20)

x = 0
y = 0
diff = 500 / 9
val = 0
#
# grid = [
#     [7, 8, 0, 4, 0, 0, 1, 2, 0],
#     [6, 0, 0, 0, 7, 5, 0, 0, 9],
#     [0, 0, 0, 6, 0, 1, 0, 7, 8],
#     [0, 0, 7, 0, 4, 0, 2, 6, 0],
#     [0, 0, 1, 0, 5, 0, 9, 3, 0],
#     [9, 0, 4, 0, 6, 0, 0, 0, 5],
#     [0, 7, 0, 3, 0, 0, 0, 1, 2],
#     [1, 2, 0, 0, 0, 7, 4, 0, 0],
#     [0, 4, 9, 2, 0, 6, 0, 0, 7]
# ]

grid = read_sudoku("sudoku.jpg")
print(grid)


def getCoordinates(pos):
    global x
    x = pos[0] // diff
    global y
    y = pos[1] // diff


def highlightCell():
    for i in range(2):
        pygame.draw.line(window, (255, 0, 0), (x * diff - 3, (y + i) * diff), (x * diff + diff + 3, (y + i) * diff), 7)
        pygame.draw.line(window, (255, 0, 0), ((x + i) * diff, y * diff), ((x + i) * diff, y * diff + diff), 7)


def createGrid():
    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:
                pygame.draw.rect(window, (0, 0, 0), (row * diff, col * diff, diff + 1, diff + 1))
                defNum = font.render(str(grid[row][col]), True, (255, 255, 255))
                window.blit(defNum, (row * diff + 15, col * diff + 15))

    for i in range(10):
        if i % 3 == 0:
            width = 3
        else:
            width = 1
        pygame.draw.line(window, (100, 100, 100), (0, i * diff), (500, i * diff), width)
        pygame.draw.line(window, (100, 100, 100), (i * diff, 0), (i * diff, 500), width)


def enterValue(v):
    num = font.render(str(v), True, (0, 0, 0))
    window.blit(num, (x * diff + 15, y * diff + 15))


def showError():
    text1 = font1.render("WRONG!", True, (0, 0, 0))
    window.blit(text1, (20, 570))


def checkInputValidity(g, i, j, v):
    for it in range(9):
        if g[i][it] == v:
            return False
        if g[it][j] == v:
            return False

    it = i // 3
    jt = j // 3

    for i in range(it * 3, it * 3 + 3):
        for j in range(jt * 3, jt * 3 + 3):
            if g[i][j] == v:
                return False

    return True


def solve(g, i, j):
    while g[i][j] != 0:
        if i < 8:
            i += 1
        elif i == 8 and j < 8:
            i = 0
            j += 1
        elif i == 8 and j == 8:
            return True

    pygame.event.pump()

    for it in range(1, 10):
        if checkInputValidity(g, i, j, it):
            g[i][j] = it
            global x, y
            x = i
            y = j

            window.fill((255, 255, 255))
            createGrid()
            highlightCell()
            pygame.display.update()
            pygame.time.delay(20)

            if solve(g, i, j) == 1:
                return True
            else:
                g[i][j] = 0

            window.fill((255, 255, 255))
            createGrid()
            highlightCell()
            pygame.display.update()
            pygame.time.delay(50)

    return False


def showInstructions():
    text1 = font1.render("PRESS R TO RESET", True, (0, 0, 0))
    text2 = font1.render("PRESS ENTER TO SOLVE", True, (0, 0, 0))
    window.blit(text1, (20, 520))
    window.blit(text2, (20, 540))


def showResult():
    text1 = font1.render("FINISHED!", True, (0, 0, 0))
    window.blit(text1, (20, 560))


run = True
flag1 = 0
flag2 = 0
rs = 0
error = 0

while run:
    window.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 1
                flag1 = 1
            if event.key == pygame.K_RIGHT:
                x += 1
                flag1 = 1
            if event.key == pygame.K_UP:
                y -= 1
                flag1 = 1
            if event.key == pygame.K_DOWN:
                y += 1
                flag1 = 1
            if event.key == pygame.K_RETURN:
                flag2 = 1
            if event.key == pygame.K_r:
                rs = 0
                error = 0
                flag2 = 0
                grid = [
                    [7, 8, 0, 4, 0, 0, 1, 2, 0],
                    [6, 0, 0, 0, 7, 5, 0, 0, 9],
                    [0, 0, 0, 6, 0, 1, 0, 7, 8],
                    [0, 0, 7, 0, 4, 0, 2, 6, 0],
                    [0, 0, 1, 0, 5, 0, 9, 3, 0],
                    [9, 0, 4, 0, 6, 0, 0, 0, 5],
                    [0, 7, 0, 3, 0, 0, 0, 1, 2],
                    [1, 2, 0, 0, 0, 7, 4, 0, 0],
                    [0, 4, 9, 2, 0, 6, 0, 0, 7]
                ]

    if flag2 == 1:
        if not solve(grid, 0, 0):
            error = 1
        else:
            rs = 1

        flag2 = 0

    if val != 0:
        enterValue(val)
        if checkInputValidity(grid, int(x), int(y), val):
            grid[int(x)][int(y)] = val
            flag1 = 0
        else:
            grid[int(x)][int(y)] = 0
            showError()

        val = 0

    if error == 1:
        showError()
    if rs == 1:
        showResult()

    createGrid()

    if flag1 == 1:
        highlightCell()

    showInstructions()

    pygame.display.update()

pygame.quit()
