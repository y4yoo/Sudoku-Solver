#!/usr/bin/env python3
"""
Assignment #6 Exercise 6
Implementing a Backtracking Sudoku Solver
"""
from copy import copy, deepcopy

def choose(S):
    min_zeros = 82
    chosen = -1
    for index, grid in enumerate(S):
        zeros = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 0:
                    zeros += 1
        if zeros < min_zeros:
            min_zeros = zeros
            chosen = index

    return S.pop(chosen)

def quadrant(x,y):
    start_x = 0
    start_y = 0

    if x < 3:
        start_x = 0
    elif x < 6:
        start_x = 3
    else:
        start_x = 6

    if y < 3:
        start_y = 0
    elif y < 6:
        start_y = 3
    else:
        start_y = 6

    return start_x,start_y

def expand(grid):
    """
    - Choose best index to expand
    - Expand by giving it 1 - 9

    """

    index_x = 0
    index_y = 0
    min_zeros = 82

    # check through all 0's
    for i in range(len(grid)):
        zeros = 0
        for j in range(len(grid[i])):
            if grid[i][j] == 0:

                # Count for surrounding 0's
                for k in range(len(grid)):
                    if grid[i][k] == 0:
                        zeros += 1
                for k in range(len(grid)):
                    if grid[k][j] == 0:
                        zeros += 1
                start_x, start_y = quadrant(i,j)
                for k in range(3):
                    x = start_x + k
                    for l in range(3):
                        y = start_y + l
                        if grid[x][y] == 0:
                            zeros += 1
                zeros -= 3 # Counted ourself 3 times
                if zeros < min_zeros:
                    min_zeros = zeros
                    index_x = i
                    index_y = j

    expanded = []
    for i in range(1,10):
        grid[index_x][index_y] = i
        expanded.append(deepcopy(grid))

    return expanded




def fails(grid):
    """
    Returns true if sudoku is wrong (whether completed or not)

    """
    for i in range(len(grid)):
        oneToNine = [1,2,3,4,5,6,7,8,9];
        for j in range(len(grid[i])):
            if grid[i][j] != 0:
                if(oneToNine.count(grid[i][j]) > 0):
                    oneToNine.remove(grid[i][j])
                else:
                    return True

    for i in range(len(grid)):
        oneToNine = [1,2,3,4,5,6,7,8,9];
        for j in range(len(grid[i])):
            if grid[j][i] != 0:
                if(oneToNine.count(grid[j][i]) > 0):
                    oneToNine.remove(grid[j][i])
                else:
                    return True

    start_x = -3
    start_y = 0
    x = 0
    y = 0
    for i in range(len(grid)):
        oneToNine = [1,2,3,4,5,6,7,8,9];
        if start_x == 6:
            start_x = 0
            start_y += 3
        else:
            start_x +=3

        for j in range(3):
            x = start_x + j
            for k in range(3):
                y = start_y + k
                if grid[x][y] != 0:
                    if(oneToNine.count(grid[x][y]) > 0):
                        oneToNine.remove(grid[x][y])
                    else:
                        return True

    return False


def succeeds(grid):
    """
    Returns true is sudoku is finished and correct
    Else returns false
    
    """
    for i in range(len(grid)):
        oneToNine = [1,2,3,4,5,6,7,8,9];
        for j in range(len(grid[i])):
            if(oneToNine.count(grid[i][j]) > 0):
                oneToNine.remove(grid[i][j])
            else:
                return False

    for i in range(len(grid)):
        oneToNine = [1,2,3,4,5,6,7,8,9];
        for j in range(len(grid[i])):
            if(oneToNine.count(grid[j][i]) > 0):
                oneToNine.remove(grid[j][i])
            else:
                return False

    start_x = -3
    start_y = 0
    x = 0
    y = 0
    for i in range(len(grid)):
        oneToNine = [1,2,3,4,5,6,7,8,9];
        if start_x == 6:
            start_x = 0
            start_y += 3
        else:
            start_x +=3

        for j in range(3):
            x = start_x + j
            for k in range(3):
                y = start_y + k
                if(oneToNine.count(grid[x][y]) > 0):
                    oneToNine.remove(grid[x][y])
                else:
                    return False

    return True

def sudoku_solver(grid):
    """
    The solver takes as input a partially completed grid
    and outputs either a completed grid, or the statement that
    no solution exists.
    
    """
    S = []
    S.append(grid)

    while len(S) > 0:
        chosen_grid = choose(S)
        subproblems = expand(chosen_grid)
        for subproblem in subproblems:
            if succeeds(subproblem):
                print_grid(subproblem)
                return subproblem
            elif not fails(subproblem):
                S.append(subproblem)

    return "no solution exists"


def print_grid(grid):
    """
    A sloppy function to print the 9 x 9 sudoku grid 
    so it's a bit easier to visualize
    """
    n = len(grid)
    for row_ind, row in enumerate(grid):
        if row_ind % 3 == 0:
            print("-----------------------------")
        for col_ind, val in enumerate(row):
            if col_ind == 8:
                print(" ", val, "|")
            elif col_ind % 3 == 0:
                print("|", val, end="")
            else:
                print(" ", val, end="")
    print("-----------------------------")


def main():
    """
    A test instance for the Sudoku Solver
    """
    # here is an easy sample grid.  0 is used for a blank.
    # each row, column, and three by three subgrid should contain
    # one of each number from 1 to 9
    grid = [[0, 0, 8, 9, 3, 0, 0, 1, 0],
            [0, 0, 5, 0, 0, 6, 3, 7, 0],
            [3, 7, 0, 0, 2, 5, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 6, 0],
            [9, 2, 1, 4, 0, 3, 8, 5, 7],
            [0, 3, 0, 0, 0, 0, 0, 0, 0],
            [0, 6, 0, 5, 9, 0, 0, 4, 8],
            [0, 9, 2, 6, 0, 0, 5, 0, 0],
            [0, 5, 0, 0, 1, 4, 9, 0, 0]
    ]

    print_grid(grid)
    print(sudoku_solver(grid))

if __name__ == '__main__':
    main()
