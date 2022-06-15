from .game import *


class TestGames:
    def test_one(self):
        game = Game()
        game.play((5,4))
        game.play((5,5))
        game.play((4,5))
        game.play((5,3))
        __import__('pdb').set_trace()
        pass

