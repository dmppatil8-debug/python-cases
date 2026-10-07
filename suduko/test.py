import pytest

from sudoku import parse, is_valid_board, can_place, solve


puzzle = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"

solved_puzzle = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"


def test_valid_board():

    grid = parse(solved_puzzle)

    assert is_valid_board(grid) is True


def test_duplicate_in_row():

    grid = parse(solved_puzzle)

    grid[0][1] = 5

    assert is_valid_board(grid) is False


def test_duplicate_in_column():

    grid = parse(solved_puzzle)

    grid[1][0] = 5

    assert is_valid_board(grid) is False


def test_duplicate_in_box():

    grid = parse(solved_puzzle)

    grid[1][1] = 5

    assert is_valid_board(grid) is False


def test_already_solved_board():

    grid = parse(solved_puzzle)

    assert solve(grid) is True
    assert is_valid_board(grid) is True


def test_unsolvable_board():

    grid = parse(puzzle)

    # 3 already exists in the first row
    grid[0][2] = 3

    assert solve(grid) is False


def test_bad_input_length():

    with pytest.raises(ValueError):
        parse("12345")


def test_solve_puzzle():

    grid = parse(puzzle)

    assert solve(grid) is True
    assert is_valid_board(grid) is True


def test_can_place():

    grid = parse(puzzle)

    # 4 can be placed at row 0, column 2
    assert can_place(grid, 0, 2, 4) is True


def test_cannot_place():

    grid = parse(puzzle)

    # 5 already exists in row 0
    assert can_place(grid, 0, 2, 5) is False