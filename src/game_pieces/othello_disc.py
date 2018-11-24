from src.game_enums import Color
from src.game_pieces.game_piece import GamePiece

class Disc(GamePiece):
    def __init__(self, color):
        super().__init__()
        self.color = color

    def __str__(self):
        return '\u26C0' if self.color == Color.WHITE else '\u26C2'

    def legal_move(self, to_coords):
        raise NotImplementedError()

    def legal_capture(self, to_coords):
        raise NotImplementedError()