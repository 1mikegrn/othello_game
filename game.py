import os

import itertools
from collections import Counter

EMPTY = "-"

def print_grid(grid):
    x, y = grid.shape
    string = "  "
    string += " ".join([str(i) for i in range(x)]) + "\n"
    for count, line in zip(range(y), grid.grid):
        string += str(count) +  " " + " ".join(line) + "\n"
    print(string)

def parse_move(move):
    move = move.split()
    if len(move) != 2:
        return None
    return tuple(map(int, move))

def walk(player, piece, grid):
    x, y = piece
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            move = (i, j)
            if chain := playable(grid, player, move, piece):
                yield move, chain

def possible_moves(player, opponent, grid):
    for piece in opponent.pieces:
        for coord in walk(player, piece, grid):
            yield coord

def move_on_board(grid, move):
    if any(i < 0 for i in move):
        return None
    x, y = move
    try:
        return grid.grid[x][y]
    except IndexError:
        return None

def same_color(grid, move, player):
    if move_on_board(grid, move) == player.name:
        return True
    return False

def playable(grid, player, move, piece):
    if move == piece:
        return None
    if not move_on_board(grid, move):
        return None
    if same_color(grid, move, player):
        return None
    delta = tuple(b-a for a, b in zip(move, piece))
    if chain := walks_to_player(player, grid, move, delta):
        return chain
    return None

def walks_to_player(player, grid, move, delta):
    chain = []
    while True:
        move = tuple(a+b for a,b in zip(move, delta))
        if not (spot := move_on_board(grid, move)):
            return False
        if spot == EMPTY:
            return False
        elif spot != player.name:
            chain.append(move)
            continue
        return chain

class Player:
    def __init__(self, name, pieces) -> None:
        self.name = name
        self.pieces = set(pieces)
        self.skip = False

    def add(self, piece):
        self.pieces.add(piece)

    def remove(self, piece):
        self.pieces.remove(piece)

class Grid:
    def __init__(self, *players, shape=(8, 8)) -> None:
        x, y = shape
        self.grid = [[EMPTY for _ in range(x)] for _ in range(y)]
        self.shape = shape

        for player in players:
            for piece in player.pieces:
                self.add(player, piece)

    def add(self, player, piece):
        x, y = piece
        self.grid[x][y] = player.name

    def remove(self, piece):
        x, y = piece
        self.grid[x][y] = EMPTY

class Game:
    def __init__(self) -> None:
        self.player = Player('b', [(3,4), (4,3)])
        self.opponent = Player('w', [(3,3), (4,4)])
        self.grid = Grid(self.player, self.opponent)

    def continues(self):
        if self.player.skip and self.opponent.skip:
            return False
        return True

    def current_player(self):
        return self.player.name

    def possible_moves(self):
        return {key: val for key, val in possible_moves(self.player, self.opponent, self.grid)}

    def next_player(self, skip=False):
        self.player.skip = skip
        self.player, self.opponent = self.opponent, self.player

    def add(self, move):
        self.player.add(move)
        self.grid.add(self.player, move)

    def capture(self, chain):
        for point in chain:
            self.add(point)
            self.opponent.remove(point)

    def print(self):
        print_grid(self.grid)


class Helper:
    def __init__(self, game, moves):
        self.name = "?"
        self.game = game
        self.moves = moves

    def __enter__(self):
        for key in self.moves.keys():
            self.game.grid.add(self, key)

    def __exit__(self, *_, **__):
        for key in self.moves.keys():
            self.game.grid.remove(key)

def main():
    game = Game()

    while game.continues():
        os.system('cls||clear')

        if not (moves := game.possible_moves()):
            print("user cannot move, skipping...")
            game.next_player(skip=True)
            continue

        with Helper(game, moves):
            game.print()

        move = input(
            f"player '{game.current_player()}': "
            "please enter your move\n>>> "
        )
        move = parse_move(move)

        if move not in moves:
            print("this is an invalid move. Please try again.")
            continue

        game.add(move)
        game.capture(moves[move])
        game.next_player()

    print("\n ### GAME OVER ### \n")

    _iter = itertools.chain.from_iterable(game.grid.grid)
    tally = Counter(_iter)
    del tally[EMPTY]

    print("final scores\n============\n")
    for k, v in sorted(tally.items(), key=lambda x: x[1], reverse=True):
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
