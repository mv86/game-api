"""Test module form game_helper module."""
from pathlib import Path

import pytest

from src.game_enums import Color, Direction
from src.games.chess import Chess
from src.games.game import adjacent_squares, Coords, move_direction
from src.game_errors import IllegalMoveError, NotOnBoardError
from src.game_pieces.pawn import Pawn


@pytest.mark.parametrize('to_coords, direction', [
    (Coords(x=6, y=6), Direction.DIAGONAL),
    (Coords(x=2, y=2), Direction.DIAGONAL),
    (Coords(x=2, y=4), Direction.HORIZONTAL),
    (Coords(x=6, y=4), Direction.HORIZONTAL),
    (Coords(x=4, y=2), Direction.VERTICAL),
    (Coords(x=4, y=6), Direction.VERTICAL),
    (Coords(x=5, y=6), Direction.NON_LINEAR),
    (Coords(x=3, y=2), Direction.NON_LINEAR),
])
def test_move_direction_correct_for_coordinates(to_coords, direction):
    from_coords = Coords(x=4, y=4)
    assert move_direction(from_coords, to_coords) == direction


def test_same_from_and_to_coords_raise_exception(game):
    from_coords = Coords(x=0, y=0)
    to_coords = Coords(x=0, y=0)
    with pytest.raises(IllegalMoveError, match=game.SAME_SQUARE):
        game.move(from_coords, to_coords)


def test_no_piece_at_from_coords_raises_exception(game):
    from_coords = Coords(x=0, y=2)
    to_coords = Coords(x=0, y=3)
    with pytest.raises(IllegalMoveError, match=game.NO_PIECE):
        # No piece passed to function
        game.move(from_coords, to_coords)


def test_attacking_piece_of_own_color_raises_exception(game):
    game.add(Pawn(Color.WHITE), Coords(x=1, y=1))
    with pytest.raises(IllegalMoveError, match=game.OWN_PIECE_ATTACK):
        # White king can't attack white Pawn
        game.move(Coords(x=0, y=0), Coords(x=1, y=1))


def test_adjacent_squares():
    assert not adjacent_squares(Coords(x=0, y=0), Coords(x=7, y=7))
    assert not adjacent_squares(Coords(x=0, y=0), Coords(x=2, y=2))
    assert adjacent_squares(Coords(x=0, y=0), Coords(x=1, y=1))
    assert adjacent_squares(Coords(x=0, y=0), Coords(x=0, y=1))


def test_can_save_game_to_file_and_load_from_file():
    file_path = Path.cwd() / 'saved_games' / 'test.pkl'

    original_game = Chess()
    original_game.save(file_path)

    restored_game = Chess.restore(file_path)
    file_path.unlink()  # Clear up test

    assert original_game == restored_game


def test_game_not_restored_for_invalid_file_path():
    file_path = Path.cwd() / 'saved_games' / 'fail.pkl'
    restored_game = Chess.restore(file_path)
    assert not restored_game
