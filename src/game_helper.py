"""Module of helper functions for games.

   Object:
        Coords: namedtuple('Coords', 'x y')

   Functions:
        move_direction: Return move direction as Direction enum type.
        legal_start_position: Check passed start coordinates are valid.
        coord_errors: Check for errors in passed board coordinates.
        coords_on_board: Check coordinates are on board.
        chess_piece_blocking: Check if piece blocking chess game move.
"""
from collections import namedtuple

from src.game_enums import Direction
from src.game_errors import InvalidMoveError, NotOnBoardError, PieceNotFoundError


Coords = namedtuple('Coords', 'x y')


def move_direction(from_coords, to_coords):
    """Calculate direction from from_coordinates to coordinates. Return Direction enum.

       Args:
            from_coords: Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1)
            to_coords:   Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1)

       Returns:
            Direction enum type
    """
    if abs(from_coords.x - to_coords.x) == abs(from_coords.y - to_coords.y):
        return Direction.DIAGONAL
    elif from_coords.x != to_coords.x and from_coords.y == to_coords.y:
        return Direction.HORIZONTAL
    elif from_coords.y != to_coords.y and from_coords.x == to_coords.x:
        return Direction.VERTICAL
    else:
        return Direction.NON_LINEAR


def legal_start_position(board, coords):
    """Check passed coordinates are valid. Return bool or raise NotOnBoardError."""
    try:
        if board[coords.x][coords.y] is None:
            return True
        return False
    except IndexError:
        raise NotOnBoardError(coords, 'Start coordinates not on board')


def check_coord_errors(piece, board, from_coords, to_coords):
    """Check for errors in passed board coordinates.

       Args:
            piece:       Game piece found at from_coords
            board:       Game board
            from_coords: Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1)
            to_coords:   Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1)

       Raises:
            NotOnBoardError:    If either passed coordinates are not in board grid.
            InvalidMoveError:   If from_coords and to_coords are the same.
            PieceNotFoundError: If no piece found at from coordinates.

    """
    if not coords_on_board(board, from_coords):
        raise NotOnBoardError(from_coords, 'From coordinates not valid board coordinates')

    if not coords_on_board(board, to_coords):
        raise NotOnBoardError(to_coords, 'To coordinates not valid board coordinates')

    if from_coords == to_coords:
        raise InvalidMoveError(from_coords, to_coords, 'Move to same square invalid')

    if not piece:
        raise PieceNotFoundError(from_coords, 'No piece found at from coordinates')


def coords_on_board(board, coords):
    """Check if coordinates within board range. Return bool"""
    if coords.x < len(board) and coords.y < len(board):
        return True
    return False


def chess_piece_blocking(board, from_coords, to_coords):
    """Check if any piece blocking move from_coords to_coords. Return bool."""
    direction = move_direction(from_coords, to_coords)
    # Sort coords so logical direction of move not important
    # (x=5, y=6) -> (x=1, y=2) same as (x=1, y=2) -> (x=5, y=6)
    min_x_coord, max_x_coord = sorted([from_coords.x, to_coords.x])
    min_y_coord, max_y_coord = sorted([from_coords.y, to_coords.y])

    if direction == Direction.NON_LINEAR:
        # Only Knights move non_linear and they can jump over pieces
        return False
    elif direction == Direction.VERTICAL:
        for next_y_coord in range(min_y_coord + 1, max_y_coord):
            if board[from_coords.x][next_y_coord] is not None:
                return True
    elif direction == Direction.HORIZONTAL:
        for next_x_coord in range(min_x_coord + 1, max_x_coord):
            if board[next_x_coord][from_coords.y] is not None:
                return True
    elif direction == Direction.DIAGONAL:
        next_y_coord = min_y_coord + 1
        for next_x_coord in range(min_x_coord + 1, max_x_coord):
            if board[next_x_coord][next_y_coord] is not None:
                return True
            next_y_coord += 1 
        
    return False  # No piece blocking
