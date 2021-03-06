import pytest

from src.games.game import Coords
from src.game_enums import Color
from src.game_pieces.othello_disc import Disc
from src.game_errors import IllegalMoveError
from src.games.othello import Othello

def test_othello_board_setup():
    game = Othello()
    expected_board_setup = set([(Color.WHITE, Coords(x=3, y=4)),
                                (Color.WHITE, Coords(x=4, y=3)),
                                (Color.BLACK, Coords(x=3, y=3)),
                                (Color.BLACK, Coords(x=4, y=4))])
    actual_board_setup = set(
        (disc.color, disc.coords)
        for row in game.board
        for disc in row if disc
    )
    assert actual_board_setup == expected_board_setup


def test_can_place_piece_and_trap_an_opponent_disc():
    game = Othello()
    assert game.board[5][3] is None
    assert game.board[4][3].color == Color.WHITE

    game.move(to_coords=Coords(x=5, y=3))
    assert game.board[5][3].color == Color.BLACK
    assert game.board[4][3].color == Color.BLACK


def test_can_trap_multiple_discs():
    game = Othello(restore_positions={
        '42': Disc(Color.WHITE),
        '43': Disc(Color.WHITE),
        '44': Disc(Color.BLACK),
        '51': Disc(Color.WHITE),
        '61': Disc(Color.WHITE),
        '71': Disc(Color.BLACK),
    })
    assert game.disc_count(Color.BLACK) == 2

    game.move(to_coords=Coords(x=4, y=1))
    assert game.disc_count(Color.BLACK) == 7


def test_player_color_swaps_for_each_turn():
    game = Othello()
    assert game.playing_color == Color.BLACK

    game.move(to_coords=Coords(x=5, y=3))
    assert game.playing_color == Color.WHITE

    game.move(to_coords=Coords(x=5, y=4))
    assert game.playing_color == Color.BLACK


def test_illegal_disc_placement_raises_exception():
    game = Othello()
    assert game.playing_color == Color.BLACK

    with pytest.raises(IllegalMoveError, match=game.SQUARE_TAKEN):
        game.move(to_coords=Coords(x=4, y=4))

    with pytest.raises(IllegalMoveError, match=game.ILLEGAL_MOVE):
        game.move(to_coords=Coords(x=5, y=4))  # doesn't trap opponent discs

    with pytest.raises(IllegalMoveError, match=game.ILLEGAL_MOVE):
        game.move(to_coords=Coords(x=7, y=7))  # not next to any discs

    assert game.playing_color == Color.BLACK  # same color to play


def test_winner_declared():
    game = Othello(restore_positions={
        '43': Disc(Color.WHITE),
        '33': Disc(Color.BLACK),
        '77': Disc(Color.WHITE),
    })
    assert not game.winner

    game.move(to_coords=Coords(x=5, y=3))
    assert game.winner == Color.BLACK


def test_drawer_declared():
    game = Othello(restore_positions={
        '00': Disc(Color.WHITE),
        '70': Disc(Color.WHITE),
        '77': Disc(Color.WHITE),
        '33': Disc(Color.BLACK),
        '34': Disc(Color.WHITE)
    })

    game.move(to_coords=Coords(x=3, y=5))
    assert game.winner == Color.NONE


def test_player_can_move_detected_correctly():
    game = Othello(restore_positions={
        '01': Disc(Color.BLACK),
        '11': Disc(Color.WHITE),
        '22': Disc(Color.BLACK)
    })
    black_can_move = game._scan_board_for_trapped_discs(Coords(x=0, y=0))
    assert black_can_move




def test_game_ends_if_both_players_cant_move():
    game = Othello(restore_positions={
        '43': Disc(Color.WHITE),
        '33': Disc(Color.BLACK),
        '77': Disc(Color.WHITE),
    })
    assert game.playing_color == Color.BLACK

    game.move(to_coords=Coords(x=5, y=3))
    assert game.winner == Color.BLACK
