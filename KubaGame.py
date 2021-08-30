# Author: Philip Peiffer
# Date: 05/21/2021
# Description: This program mimics playing the "Kuba" game with the following classes:
# KubaGame - contains 2 player objects, a board object, and a winner name. Contains methods to interact with the game
# Player - contains attributes for player_name, marble_color, whether it's their turn, and number of captured neutral
#          marbles. Has methods to get and set those attributes
# Board - contains attributes _board and _prev_board. Initializes the _board to the starting position and stores the
#         previous move's board for the "Ko rule" comparison. Contains methods for getting marbles a various number
#         of ways to support the KubaGame and Player classes as well as a method for moving the marbles and returning
#         the "next board" for the Ko rule comparison.

class Player:
    """Represents a player of the game. Contains an init method that creates a new player instance with marble color
    and player name required as inputs. Each player has 4 attributes (name, marble color, turn, and captured marble
    count). Contains get and set methods for these attributes as well as an add_captured_marble_count method that
    adds 1 to the captured_marble_count."""
    def __init__(self, player_name, marble_color):
        """Creates a new player for the game. Requires inputs for the player name (string) and player color (W or B).
        Initializes the "turn" attribute to True to start the game (switches between True and False when it is or is
        not that player's turn respectively). Initializes the captured_marble_count attribute to 0."""
        self._player_name = player_name
        self._marble_color = marble_color
        self._turn = True
        self._captured_marble_count = 0         # counts the NEUTRAL marbles captured

    def get_player_marble_count(self, board):
        """Returns the marble count of a player on the current board. Requires a board object as input. The board object
        comes from the KubaGame class."""
        if self._marble_color == "W":
            marble_count = board.get_marble_count()[0]
        else:
            marble_count = board.get_marble_count()[1]
        return marble_count

    def get_player_name(self):
        """Returns a player's name."""
        return self._player_name

    def get_turn(self):
        """Returns True if it's the player's turn, False if it's not the player's turn."""
        return self._turn

    def set_turn(self, bool_input):
        """Requires a boolean input of true or false and updates the player's turn attribute. True = it is that player's
        turn. False = it is not that player's turn."""
        self._turn = bool_input

    def get_marble_color(self):
        """Returns the marble color of a player. No input required."""
        return self._marble_color

    def get_captured_marble_count(self):
        """Returns the number of neutral marbles captured by the player."""
        return self._captured_marble_count

    def add_captured_marble_count(self):
        """Adds 1 to the captured marble count. No input and no return."""
        self._captured_marble_count += 1


class KubaGame:
    """Represents a game of Kuba. Each game is initialized with 2 player objects of the Player class, a starting board
     object of the Board class, and a winner value of None. Each instance of the game contains methods as follows:
     make_move, get_current_turn, update_current_turn, get_marble, get_captured, get_marble_count, get_winner,
     next_legal_move, move_permission, get_player_by_name, and print_board."""

    def __init__(self, *args):
        """Creates a new Kuba game. Requires a tuple input of (player_name (str), marble_color (W or B)) for two
        players. Creates a list of the players as instances of the Player class and initializes the board with an
        instance of the Board class. Initializes the winner to None."""
        self._players = []
        # loop through the tuple input and create player objects for each player, assign them to the list of players
        for tuple_input in args:
            self._players.append(Player(tuple_input[0], tuple_input[1]))
        self._board = Board()
        self._winner = None

    def get_player_by_name(self, player_name):
        """Returns the player object that matches the player name."""
        for player in self._players:
            if player.get_player_name() == player_name:
                return player

    def get_current_turn(self):
        """Returns the player's name whose turn it currently is. If no one has played a move yet, returns None."""
        player1 = self._players[0]
        player2 = self._players[1]
        if player1.get_turn() == player2.get_turn():
            return None
        elif player1.get_turn():
            return player1.get_player_name()
        else:
            return player2.get_player_name()

    def update_current_turn(self, player):
        """Requires an input of the player object that just took a turn. Updates the turn attribute of the players so
        that the next player has a value of True."""
        player1 = self._players[0]
        player2 = self._players[1]
        if player1 == player:
            player1.set_turn(False)
            player2.set_turn(True)
        else:
            player1.set_turn(True)
            player2.set_turn(False)

    def get_marble(self, coord):
        """Returns the color of a marble in the space on the board represented by the coordinate input by the user. The
        coordinate must be in tuple format (row, col) with the row and col count starting at 0. If no marble is present
        returns 'X'."""
        return self._board.get_marble(coord)

    def get_captured(self, player_name):
        """Takes a player name as input and returns the number of neutral marbles captured by that player."""
        player_obj = self.get_player_by_name(player_name)
        return player_obj.get_captured_marble_count()

    def get_marble_count(self):
        """Returns the number of white, black, and red marbles still on the board in a tuple in that order."""
        return self._board.get_marble_count()

    def next_legal_move(self, player):
        """Requires a player object input and determines if that player has any legal moves available. Returns True if
        a player has a legal move on the current board. Returns False otherwise."""
        # find where the player's marbles are on the board
        player_marble_coords = self._board.get_marble_coords(player)
        # save the starting turn value so that we after checking permissions we can set it back to original
        player_turn = player.get_turn()

        # check permission method for every marble on the board. If a legal move is found, return True
        for coord in player_marble_coords:
            # need to overwrite the turn to True so that we don't fail on not being their turn
            player.set_turn(True)

            # check permission for every direction
            if (self.move_permission(player, coord, "L") or self.move_permission(player, coord, "R")
                    or self.move_permission(player, coord, "F") or self.move_permission(player, coord, "B")):

                # update the current turn to original and return True
                player.set_turn(player_turn)
                return True

        # if we've made it to the end without returning (finding a legal move), return False
        player.set_turn(player_turn)
        return False

    def move_permission(self, player, play_coord, direction):
        """Requires a player object, a coordinate of where a play is starting from (in tuple format of (row, col) and
        (0, 0) being the top left corner), and the direction of the marble push (R, L, F, or B) as input. Determines
        if the move is permissible and returns True if it is, otherwise returns False. A move is not permissible if
        it results in undoing the previous player's move, if it's not that player's turn, if a winner has been crowned,
        if the player is not pushing on their own marble, if a move would result in the player's own color falling off
        the board, or if the marble that they're pushing does not have an empty spot adjacent to and opposite from the
        motion of the push (e.g. a marble at (1,1) being pushed right has to have an empty spot at (1,0))."""
        prev_board = self._board.get_prev_board()
        move_marbles = self._board.move_marbles(play_coord, player, direction, self.get_marble(play_coord))
        next_board = move_marbles[1]
        own_marble_captured = move_marbles[2]

        if direction == "L":
            blank_space = (play_coord[0], play_coord[1] + 1)
            board_edge = len(self._board.get_current_board()[play_coord[0]]) - 1
            start_index = play_coord[1]

        elif direction == "R":
            blank_space = (play_coord[0], play_coord[1] - 1)
            board_edge = 0
            start_index = play_coord[1]

        elif direction == "F":
            blank_space = (play_coord[0] + 1, play_coord[1])
            board_edge = len(self._board.get_current_board()[play_coord[0]]) - 1
            start_index = play_coord[0]

        else:
            blank_space = (play_coord[0] - 1, play_coord[1])
            board_edge = 0
            start_index = play_coord[0]

        # check to make sure it's their turn
        if not player.get_turn():
            return False

        # check to make sure no one else has won
        elif self._winner is not None:
            return False

        # check to make sure that the player is playing their color
        elif player.get_marble_color() != self.get_marble(play_coord):
            return False

        # check to make sure that the space adjacent to the marble is empty OR that it's at the edge of the board
        elif start_index != board_edge and self.get_marble(blank_space) != "X":
            return False

        # check to make sure they won't knock their own color off
        elif own_marble_captured:
            return False

        # check to make sure moving the marbles right doesn't undo the previous player's move
        elif next_board == prev_board:
            return False

        else:
            return True

    def get_winner(self):
        """This function requires no input. Determines if a winner has been crowned. If so, returns that player's
        name, otherwise returns None. A winner is crowned if any of the following occur: that player has collected 7
        neutral balls, the opposing player has run out of legal moves, or the player has knocked off all of the opposing
        player's balls."""
        # if the winner has already been crowned, just return the winner
        if self._winner is not None:
            return self._winner
        else:
            # find the winner
            # define the players
            player_one = self._players[0]
            player_two = self._players[1]
            # how do we win?
            # if we capture 7 neutral balls
            for player in self._players:
                if player.get_captured_marble_count() == 7:
                    self._winner = player.get_player_name()
                    return self._winner

            # if we knock off all of the opponents ball
            p1_marble_count = player_one.get_player_marble_count(self._board)
            p2_marble_count = player_two.get_player_marble_count(self._board)

            if p1_marble_count == 0:
                self._winner = player_two.get_player_name()
                return self._winner
            if p2_marble_count == 0:
                self._winner = player_one.get_player_name()
                return self._winner

            # if the opponent cannot move
            if not self.next_legal_move(player_one):
                self._winner = player_two.get_player_name()
                return self._winner
            if not self.next_legal_move(player_two):
                self._winner = player_one.get_player_name()
                return self._winner

    def make_move(self, player_name, play_coord, direction):
        """Takes a coordinate in tuple format of the marble that the player would like to push from, the NAME of the
        player making the move, and the direction they wish to move. Directions can either be: L (left) R (right)
        F (forward) or B (backward). If the move is successful, updates the current turn, updates the captured marble
        count of the player, and determines if a winner has been crowned. Returns True if the move was successful,
        otherwise returns false."""
        player_obj = self.get_player_by_name(player_name)
        move_marbles_return = self._board.move_marbles(play_coord, player_obj, direction, self.get_marble(play_coord))

        # check permission to move
        if self.move_permission(player_obj, play_coord, direction):
            # grab the next board
            next_board = move_marbles_return[1]

            # copy the current board
            current_board = self._board.copy_board(self._board.get_current_board())

            # set the current board to the previous board, and the next board to the current board
            self._board.set_prev_board(current_board)
            self._board.set_current_board(next_board)

            # if a marble was captured, update the marble_captured count
            if move_marbles_return[0]:
                player_obj.add_captured_marble_count()

            # update the current turn
            self.update_current_turn(player_obj)

            # determine if a winning move was made
            self.get_winner()
            return True
        else:
            return False

    def print_board(self):
        """This function prints the board for easier troubleshooting"""
        for row in self._board.get_current_board():
            print(row)


class Board:
    """Represents a board of a Kuba game. Initializes the board per the game instructions and keeps track of the
    marble positions throughout the game. Contains two private data members (board and prev_board).
    Contains methods as follows: get_current_board, set_current_board, get_prev_board, set_prev_board, copy_board,
    get_marble, get_marble_coords, and move_marbles. Interacts with the Player class on certain methods as they
    require a player object as input to return the correct information."""

    def __init__(self):
        """Creates a new game board and initializes it per the game instructions. No input required. The board is
        modeled as a list of lists. Each row is a separate list. Each marble is represented by its color. Initializes
        the prev_board to None."""
        self._board = [
            ['W', 'W', '-', '-', '-', 'B', 'B'],
            ['W', 'W', '-', 'R', '-', 'B', 'B'],
            ['-', '-', 'R', 'R', 'R', '-', '-'],
            ['-', 'R', 'R', 'R', 'R', 'R', '-'],
            ['-', '-', 'R', 'R', 'R', '-', '-'],
            ['B', 'B', '-', 'R', '-', 'W', 'W'],
            ['B', 'B', '-', '-', '-', 'W', 'W']
        ]
        self._prev_board = None

    def get_current_board(self):
        """Returns the current board as a list of lists."""
        return self._board

    def set_current_board(self, board):
        """Requires a list of lists representing a board as input and sets the current board to that list. Used in this
        program after the move permissions have passed to set the next_board from the move_direction methods to the
        current board"""
        self._board = board

    def get_prev_board(self):
        """Returns the previous move's board as a list of lists."""
        return self._prev_board

    def set_prev_board(self, prev_board):
        """Requires a list of lists as input representing the state of the board and sets the prev_board attribute
        equal to the input."""
        self._prev_board = prev_board

    def copy_board(self, current_board):
        """Requires a board (list of lists) as input and returns a deep copy."""
        copied_board = []
        for row in current_board:
            copied_row = []
            for space in row:
                copied_row.append(space)
            copied_board.append(copied_row)
        return copied_board

    def get_marble(self, coordinate):
        """Returns the marble color at a board coordinate specified in the input. Input must be in tuple format
        (e.g. (row, column)) in list index numbering. If no marble is present returns an "X"."""
        # check to make sure there is a marble at the location
        if self._board[coordinate[0]][coordinate[1]] != "-":
            return self._board[coordinate[0]][coordinate[1]]
        else:
            return "X"

    def get_marble_coords(self, player):
        """Requires a player object as input and returns the location of their marbles as a list with coordinates in
        tuple format (row, column)"""
        marble_coords = []
        for row_index in range(len(self._board[0])):
            for col_index in range(len(self._board[0])):
                if self.get_marble((row_index, col_index)) == player.get_marble_color():
                    marble_coords.append((row_index, col_index))
        return marble_coords

    def get_marble_count(self):
        """Returns the number of white, black, and red marbles still on the board in a tuple in that order."""
        white_marb = 0
        black_marb = 0
        red_marb = 0
        for row in self._board:
            for space in row:
                if space == 'W':
                    white_marb += 1
                elif space == 'B':
                    black_marb += 1
                elif space == 'R':
                    red_marb += 1
        return white_marb, black_marb, red_marb

    def move_marbles(self, play_coord, player, direction, current_marble, next_board=None):
        """Takes a coordinate in tuple format of the marble that the player would like to push from (with (0, 0) being
        the top left corner of the board), the player object making the move, the direction they wish to move (L, R, F,
        or B), and the current_marble. Current_marble should always be initialized to the marble color at the starting
        coordinates. Loops through the marbles that are adjacent to each other through use of a recursive function,
        passing the adjacent marble in for the current_marble in each loop. Once a blank space or edge of the board
        is reached, returns a tuple with 3 values: marble_captured (True if the player has knocked off a neutral red
        ball, False otherwise), next_board (list of lists showing what the next move will look like), and
        own_marble_captured (True if the player has knocked off their own color of marble, False otherwise)."""

        play_row = play_coord[0]
        play_col = play_coord[1]
        neut_marble_captured = False
        own_marble_captured = False

        # at the start of the recursion copy the board to next_board so that we modify next_board instead of
        # the current board. Only want to move marbles right if we pass the permissions
        if next_board is None:
            next_board = self.copy_board(self._board)
            # if we're on the first move, a blank space will replace the current_marble that shifted to the next spot
            next_board[play_row][play_col] = '-'

        if direction == "L" or direction == "R":
            if direction == "L":
                next_marble_coord = (play_row, play_col - 1)
            else:
                next_marble_coord = (play_row, play_col + 1)
            # if we hit the end of the list or the end of marble line, end the recursion and return marble_captured
            if next_marble_coord[1] < 0 or next_marble_coord[1] == len(self._board[play_row]) or current_marble == "X":
                # if we're on the last col and current_marble is R, update marble_captured to True
                if current_marble == "R":
                    neut_marble_captured = True
                # if we're on the last col and current_marble is same color as player color, update own_marble_captured
                # to True
                if current_marble == player.get_marble_color():
                    own_marble_captured = True
                return neut_marble_captured, next_board, own_marble_captured

        elif direction == "F" or direction == "B":
            if direction == "F":
                next_marble_coord = (play_row - 1, play_col)
            else:
                next_marble_coord = (play_row + 1, play_col)
            if next_marble_coord[0] < 0 or next_marble_coord[0] == len(self._board[play_row]) or current_marble == "X":
                if current_marble == "R":
                    neut_marble_captured = True
                if current_marble == player.get_marble_color():
                    own_marble_captured = True
                return neut_marble_captured, next_board, own_marble_captured

        # grab the marble color next to current_marble before we overwrite it
        next_marble = self.get_marble(next_marble_coord)

        # shift the current marble over into the next_marble spot
        next_board[next_marble_coord[0]][next_marble_coord[1]] = current_marble

        # run again
        return self.move_marbles(next_marble_coord, player, direction, next_marble, next_board)


if __name__ == "__main__":
    game = KubaGame(("p1", "B"), ("p2", "W"))

    def make_move_decorator(func):
        """Decorates a move in the console for easier troubleshooting"""
        def wrapper(*args, **kwargs):
            """provides decoration for make_move function. Requires make_move inputs."""
            print("========================= making move ====================================")
            print(game.get_current_turn(), "turn")
            func(*args, **kwargs)
            game.print_board()
            print(game.get_marble_count())
            print("winner:", game.get_winner())
            for player in game._players:
                print(player.get_player_name())
                print(player.get_captured_marble_count())
            print("next turn:", game.get_current_turn())

        return wrapper


    @make_move_decorator
    def move(player_name, play_coord, direction):
        game.make_move(player_name, play_coord, direction)
