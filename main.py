import random, copy


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


class Node(object):

    inevitable_loss = 0
    inevitable_win = 1
    inevitable_nothingness = 2

    def __init__(self, board_state, move=None, height=0, parent=None):

        # for help knowing which piece is played per level
        self.height = height

        # for making the move when the time comes. the difference between the upper level and this state
        self.move = move

        self.board_state = board_state

        self.type = Node.inevitable_nothingness

        self.parent = parent

        self.nodes = []


class Ai(Player):
    def __init__(self, character):
        Player.__init__(self, character)

        # we will create a tree spanning all possible moves in this game.

        tmp_board = Board()
        self.tree_index = self.tree = Node(tmp_board)
        self.make_tree(self.tree)

        self.score_tree(self.tree_index, character)

        print("i am all prepared. you shall be defeated!!!")

    def score_tree(self, node, character):
        # at each node, compute the number of winning moves and total moves in its branches
        # the score of this node is the sum of the scores of the leaf nodes

        # base case. leaf node. return whether this is victory or not
        if len(node.nodes) == 0:
            if self.is_our_victory(node.board_state.board, character):
                node.type = Node.inevitable_win
            elif self.is_our_victory(node.board_state.board, 'X' if character == 'O' else 'X'):
                node.type = Node.inevitable_loss
                node.parent.type = Node.inevitable_loss

        for leaf in node.nodes:
            self.score_tree(leaf, character)

    def is_our_victory(self, board, character):
        # check for horizontal victory
        for row in board:
            if all_same(row[0], row[1], row[2]) and row[0] == character:
                return True

        # check for vertical victory
        for i in range(0, 3):
            if all_same(board[0][i], board[1][i], board[2][i]) and board[0][i] == character:
                return True

        # check for diagonal victory
        if all_same(board[0][0], board[1][1], board[2][2]) and board[0][0] == character:
            return True

        if all_same(board[0][2], board[1][1], board[2][0]) and board[1][1] == character:
            return True

        return False

    def make_tree(self, node):
        for move in self.get_possible_moves(node.board_state.board):
            tmp_clone = copy.deepcopy(node.board_state)
            tmp_clone.set_piece(move[0], move[1], 'X' if node.height % 2 == 0 else 'O')
            node.nodes.append(Node(tmp_clone, move=move, height=node.height + 1, parent=node))

        for leaf in node.nodes:
            # if this node results in an enemy victory, dont even bother!
            # if self.is_our_victory(leaf.board_state.board, 'X' if self.character != 'X' else 'O'):
            #     node.score = -10000
            #     node.nodes = []
            #     return

            if not leaf.board_state.game_over():
                self.make_tree(leaf)

    def get_possible_moves(self, board):
        """
        returns all open spaces left on the board, as a list of tuples
        :param board:
        :param character:
        :return:
        """
        moves = []
        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                if board[i][j] == ' ':
                    moves.append((i, j))

        return moves

    def go(self, board):
        # from our stored position in our big tree, advance to the next level based on the current state of the board
        if board != self.tree_index.board_state:
            for i in range(0, len(self.tree_index.nodes)):
                if board == self.tree_index.nodes[i].board_state:
                    self.tree_index = self.tree_index.nodes[i]
                    break

        # error checking: no moves possible
        if 0 == len(self.tree_index.nodes):
            return

        # if there is an inevitable victory: take it.
        best = None
        for leaf in self.tree_index.nodes:
            if Node.inevitable_win == leaf.type:
                best = leaf
                break

        # otherwise, take a non-inevitable loss choice
        if best is None:
            for leaf in self.tree_index.nodes:
                if Node.inevitable_loss != leaf.type:
                    best = leaf
                    break

        # if best is still None, it means we lose. capitulate!
        if best is None:
            print("you win! i capitulate")
            exit()

        # advance our internal pointer and return that one
        if board.set_piece(best.move[0], best.move[1], self.character):
            self.tree_index = best
            print("take that!")
        else:
            print("something went wrong! i couldnt make my evil move!")
            exit()


class Board(object):
    def __init__(self):
        self.board = []
        for i in range(0, 3):
            self.board.append([' ', ' ', ' '])

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False


        for i in range(0, 3):
            for j in range(0, 3):
                if self.board[i][j] != other.board[i][j]:
                    return False
        return True

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

    # game over, let's see who won!
    board.display()