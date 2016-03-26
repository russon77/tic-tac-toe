import random


class Player(object):
    def __init__(self, character):
        self.character = character


class Human(Player):
    def go(self, board):
        while True:
            x = int(input('X: '))
            y = int(input('Y: '))

            if board.set_piece(y, x, self.character):
                return True


class Ai(Player):
    def go(self, board):
        print('im thinking very hard....')
        while True:
            if board.set_piece(random.randint(0, 2), random.randint(0, 2), self.character):
                return True


class Board(object):
    def __init__(self):
        self.board = []
        for i in range(0, 3):
            self.board.append([' ', ' ', ' '])

    def set_piece(self, x, y, character):
        # bounds check
        if x < 0 or x > 2:
            return False
        if y < 0 or y > 2:
            return False

        if self.board[x][y] == ' ':
            self.board[x][y] = character
            return True

        return False

    def display(self):
        for row in self.board:
            print('|' + row[0] + '|' + row[1] + '|' + row[2] + '|')

    def game_over(self):

        # check for horizontal victory
        for row in self.board:
            if all_same(row[0], row[1], row[2]) and row[0] != ' ':
                return True

        # check for vertical victory
        for i in range(0, 3):
            if all_same(self.board[0][i], self.board[1][i], self.board[2][i]) and self.board[0][i] != ' ':
                return True

        # check for diagonal victory
        if all_same(self.board[0][0], self.board[1][1], self.board[2][2]) and self.board[0][0] != ' ':
            return True

        if all_same(self.board[0][2], self.board[1][1], self.board[2][0]) and self.board[1][1] != ' ':
            return True

        return False

    def filled(self):
        for row in self.board:
            for tile in row:
                if tile == ' ':
                    return False

        return True


def all_same(*args):
    if 0 == len(args):
        return True

    running = args[0]
    for i in range(1, len(args)):
        if args[i] != running:
            return False

    return True


if __name__ == '__main__':
    players = [Human('X'), Ai('O')]
    board = Board()

    player_index = 0

    while not board.game_over() and not board.filled():
        board.display()

        current_player = players[player_index]

        current_player.go(board)

        player_index = (player_index + 1) % 2
