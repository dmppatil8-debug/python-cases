solve_calls = 0


def parse(puzzle):
    if len(puzzle) != 81:
        raise ValueError("Puzzle must have 81 characters")

    grid = []

    for i in range(0, 81, 9):
        row = []

        for char in puzzle[i:i + 9]:
            row.append(int(char))

        grid.append(row)

    return grid


def is_valid_board(grid):

    # Check rows
    for row in grid:
        numbers = []

        for num in row:
            if num != 0:
                if num in numbers:
                    return False

                numbers.append(num)

    # Check columns
    for col in range(9):
        numbers = []

        for row in range(9):
            num = grid[row][col]

            if num != 0:
                if num in numbers:
                    return False

                numbers.append(num)

    # Check 3x3 boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):

            numbers = []

            for row in range(box_row, box_row + 3):
                for col in range(box_col, box_col + 3):

                    num = grid[row][col]

                    if num != 0:
                        if num in numbers:
                            return False

                        numbers.append(num)

    return True


def can_place(grid, row, col, digit):

    # Check row
    for i in range(9):
        if grid[row][i] == digit:
            return False

    # Check column
    for i in range(9):
        if grid[i][col] == digit:
            return False

    # Find the starting position of the 3x3 box
    start_row = 3 * (row // 3)
    start_col = 3 * (col // 3)

    # Check box
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):

            if grid[i][j] == digit:
                return False

    return True


def solve(grid):

    global solve_calls
    solve_calls += 1

    # Find an empty cell
    for row in range(9):
        for col in range(9):

            if grid[row][col] == 0:

                # Try numbers 1 to 9
                for digit in range(1, 10):

                    if can_place(grid, row, col, digit):

                        # Put the number
                        grid[row][col] = digit

                        # Try solving the rest of the board
                        if solve(grid):
                            return True

                        # Number didn't work, so undo it
                        grid[row][col] = 0

                # No number worked for this cell
                return False

    # No empty cells left
    return True


def show(grid):

    print("+-------+-------+-------+")

    for row in range(9):

        print("|", end=" ")

        for col in range(9):

            num = grid[row][col]

            if num == 0:
                print(".", end=" ")
            else:
                print(num, end=" ")

            if col == 2 or col == 5:
                print("|", end=" ")

        print("|")

        if row == 2 or row == 5:
            print("+-------+-------+-------+")

    print("+-------+-------+-------+")


# Test puzzle
puzzle = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"

grid = parse(puzzle)

print("Original Sudoku:")
show(grid)

print("\nValid board:", is_valid_board(grid))

solve_calls = 0

if solve(grid):
    print("\nSudoku solved!")
else:
    print("\nNo solution exists.")

print("Solve calls:", solve_calls)

print("\nSolution:")
show(grid)

print("Solution is valid:", is_valid_board(grid))