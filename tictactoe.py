"""
Tic Tac Toe Player
"""

import math
import copy
import sys
import random

X = "X"
O = "O"
EMPTY = None


### My custom Exceptions ###
class InvalidActionError(Exception):
    """ Raised when the action is invalid """
    pass


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


# Return the player that should make a move now
# Raise the InvalidBoardError if the board is not valid
def player(board):
    """
    Returns player who has the next turn on a board.
    """

    x_count = 0
    o_count = 0

    for row in board:
        for tile in row:
            if tile == X:
                x_count += 1
            elif tile == O:
                o_count += 1

    if x_count == o_count:
        return X
    else:
        return O


# Return a list of possible actions on the current board
# Return None if the board is in terminal state
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    if terminal(board):
        return None

    actions_list = []

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions_list.append((i, j))

    return actions_list


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if board[action[0]][action[1]] != EMPTY:
        raise InvalidActionError

    # make a deep copy of the board
    board_copy = copy.deepcopy(board)

    # may raise the InvalidBoardError exception
    board_copy[action[0]][action[1]] = player(board_copy)

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for i in range(3):
        # check rows
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        # check columns
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]

    # check left up to right bottom diagnol
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    # check right up to left bottom diagnol
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    # no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # there is a winner
    if winner(board):
        return True

    for i in range(3):
        for j in range(3):
            # if no winner found and have empty cell on board, means game is still on going
            if board[i][j] == EMPTY:
                return False

    # no winner, board full, means a draw
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    ttt_winner = winner(board)
    if ttt_winner == X:
        return 1
    elif ttt_winner == O:
        return -1
    return 0


def get_best_utility_value(board, parent_optimal_util):
    """
    Returns the optimal utility value for the current player on the board.
    Use the parent_optimal_util value to perform alpha-beta pruning
    """

    if terminal(board):
        return utility(board)

    current_player = player(board)

    if current_player == X:  # max
        local_max_util = -sys.maxsize - 1
        available_actions = actions(board)

        # shuffle the actions list to make AI looks more alive
        random.shuffle(available_actions)

        for action in available_actions:
            # make the move
            res = result(board, action)
            temp_util = get_best_utility_value(res, local_max_util)

            if temp_util == 1:
                return 1

            # alpha-beta pruning
            # last call was by the min player
            # so if there is a greater utility value in this branch just stop finding
            if temp_util > parent_optimal_util:
                return parent_optimal_util

            # if there is a better action, update the best_action and the local_max_util
            local_max_util = max(temp_util, local_max_util)

        return local_max_util

    else:  # min
        local_min_util = sys.maxsize
        available_actions = actions(board)

        # shuffle the actions list to make AI looks more alive
        random.shuffle(available_actions)

        for action in available_actions:
            # make the move
            res = result(board, action)
            temp_util = get_best_utility_value(res, local_min_util)

            if temp_util == -1:
                return -1

            # alpha-beta pruning
            # last call was by the max player
            # so if there is a smaller utility value in this branch just stop finding
            if temp_util < parent_optimal_util:
                return parent_optimal_util

            # if there is a better action, update the best_action and the local_min_util
            local_min_util = min(temp_util, local_min_util)

        return local_min_util


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    current_player = player(board)

    if current_player == X:  # max
        local_max_util = -sys.maxsize - 1
        available_actions = actions(board)

        # shuffle the actions list to make AI looks more alive
        random.shuffle(available_actions)

        # if board is empty
        if len(available_actions) == 9:
            return available_actions[0]

        best_action = ()
        for action in available_actions:
            # make the move
            res = result(board, action)
            temp_util = get_best_utility_value(res, local_max_util)

            if temp_util == 1:
                return action

            # if there is a better action, update the best_action and the local_max_util
            if temp_util > local_max_util:
                local_max_util = temp_util
                best_action = action

        return best_action

    else:  # min
        local_min_util = sys.maxsize
        available_actions = actions(board)

        # shuffle the actions list to make AI looks more alive
        random.shuffle(available_actions)

        best_action = ()
        for action in available_actions:
            # make the move
            res = result(board, action)
            temp_util = get_best_utility_value(res, local_min_util)

            if temp_util == -1:
                return action

            # if there is a better action, update the best_action and the local_min_util
            if temp_util < local_min_util:
                local_min_util = temp_util
                best_action = action

        return best_action
