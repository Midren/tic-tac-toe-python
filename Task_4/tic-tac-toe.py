from btree import Tree
from btnode import Node
from copy import deepcopy


class Board:
    """
    Represents board for tic-tac-toe game
    """
    PLAYER_ONE_SIGN = "X"
    PLAYER_TW0_SIGN = "O"

    PLAYER_SIGNS = [PLAYER_ONE_SIGN, PLAYER_TW0_SIGN]

    def __init__(self):
        """
        Initialize board with blank space
        """
        self.field = [[" " for _ in range(3)] for __ in range(3)]

    def __str__(self):
        """
        Returns str representation of board
        """
        res = "  a b c\n"
        res = res + "\n  -----\n".join(
                [str(i + 1) +" " + "|".join(self.field[i]) for i in range(3)])
        return res

    def is_full(self):
        """
        Checks if board is full
        """
        for x in range(3):
            for y in range(3):
                if self.field[x][y] == ' ':
                    return False
        return True

    def winner_sign(self):
        """
        Returns sign of winner if there is someone or None either
        """
        win_column = False
        for j in range(3):
            for i in range(2):
                if (self.field[i][j] != self.field[i + 1][j] or
                        self.field[i][j] == ' '):
                    break
            else:
                win_column = self.field[i][j]
                break
        if win_column:
            return win_column

        win_line = False
        for i in range(3):
            for j in range(2):
                if (self.field[i][j] != self.field[i][j + 1] or
                        self.field[i][j] == ' '):
                    break
            else:
                win_line = self.field[i][j]
                break

        if win_line:
            return win_line

        elif (self.field[0][0] == self.field[1][1] == self.field[2][2] or
              self.field[2][0] == self.field[1][1] == self.field[0][2]) and \
                self.field[1][1] != " ":
            return self.field[1][1]
        else:
            return None


class Game:
    """
    Represents a tic-tac-toe game
    """

    def __init__(self, player1, player2):
        """
        Initialize a game with board and players
        """
        self.players = [player1, player2]
        self.field = Board()
        self.current = 0

    def play(self):
        """
        Starts game in console mode
        """
        while not self.field.is_full():
            print(self.field)
            self.players[self.current].make_step(self.field, self.current)
            if self.field.winner_sign():
                print(self.field)
                self.players[self.current].print_win()
                return
            self.current = (self.current + 1) % 2
        print("Oh, it's a draw")


class Player:
    """
    Represents a Player in table game
    """

    def __init__(self, name):
        """
        Initialize a player with a name
        """
        self.name = name

    def make_step(self, field, current):
        """
        Makes step on field
        """
        raise NotImplementedError("Abstract class")

    def print_win(self):
        """
        Print message to winner
        """
        print("Congratulations to Player " + str(self.name) + "!")


def win_rate(tree, win_player, cur_player=None):
    """
    Calculate winrate of player using tree of game
    """
    if cur_player is None:
        cur_player = win_player
    if len(tree.childs) == 0:
        if tree.data.is_full():
            return 0
        elif Board.PLAYER_SIGNS.index(tree.data.winner_sign()) == win_player:
            return 1
        else:
            return -1
    else:
        cur_player = (1 + cur_player) % 2
        if win_player == cur_player:
            return max([win_rate(node, win_player, cur_player) for node in
                        tree.childs])
        else:
            return min([win_rate(node, win_player, cur_player) for node in
                        tree.childs])


class HumanPlayer(Player):
    """
    Represents a Human Player in tic-tac-toe
    """

    def make_step(self, field, current):
        """
        Makes step on field
        """
        while True:
            step = input("Make your step, Player " + str(self.name) +
                         " (Example: a1): ").lower()
            if not (0 < len(step) < 3):
                print("Invalid input")
                continue
            elif not step[0].isalpha() or not step[1].isnumeric():
                print("Invalid input")
                continue
            elif not ord("a") <= ord(step[0]) <= ord("c") or not 0 < int(
                    step[1]) < 4:
                print("Invalid input")
                continue
            elif field.field[int(step[1]) - 1][ord(step[0]) - ord("a")] != " ":
                print("Invalid input")
                continue
            else:
                break
        field.field[int(step[1]) - 1][ord(step[0]) - ord("a")] = \
        Board.PLAYER_SIGNS[current]


class CleverBotPlayer(Player):
    """
    Represents a high skill bot in tic-tac-toe game
    """

    def make_step(self, field, current, cur_node=None):
        """
        Makes step on field
        """
        fst = False
        new_node = Tree(field)
        if cur_node == None:
            cur_node = new_node
            fst = True

        if field.is_full() or field.winner_sign():
            cur_node.add_node(Node(field))

        for x in range(3):
            for y in range(3):
                if field.field[x][y] == " ":
                    field.field[x][y] = Board.PLAYER_SIGNS[current]
                    self.make_step(deepcopy(field), (current + 1) % 2,
                                   new_node)
                    field.field[x][y] = " "

        if fst:
            win_rates = [win_rate(node, current) for node in new_node.childs]
            step = win_rates.index(max(win_rates))
            field.field = new_node.childs[step].data.field
            return
        else:
            cur_node.add_node(new_node)

        return cur_node

if __name__ == "__main__":
	gm = Game(HumanPlayer("1"), CleverBotPlayer("2"))
	gm.play()
