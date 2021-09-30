from enum import Enum
import numpy as np
from .node import BoardNode

class Action(Enum):
    L = 0
    R = 1
    U = 2
    D = 3

class Puzzle:

    EMPTY = "_"
    GOAL = np.array([['1', '2', '3'],
                     ['4', '5', '6'],
                     ['7', '8', '_']])

    @staticmethod
    def initialize(state_file):
        f = open(state_file, "r")
        plist = []
        for s in f.readlines():
            plist.extend(s.split())

        board = np.empty((3,3), dtype=str)
        board[0] = plist[:3]
        board[1] = plist[3:6]
        board[2] = plist[6:]

        print(f"Initialized board:\n{board}")
        print(f"Starting location: {Puzzle.pos_str(board)}\n\n")

        return BoardNode(board)

    @staticmethod
    def get_inversions(board):
        """
        Returns the current amount of inversions.

        An inversion is when a larger number is before a smaller number.
        Ex. If the board state is [1, 2, 4, 8, _, 5, 6, 7, 3],
            then the inversions are (4, 3), (8, 5), (8, 6), (8, 3), (7, 3)

        If there are no inversions, the game is won. If there is an odd number
        of inversions, the game is not solvable.

        Args:
            board (numpy.ndarray): Array representing the board state.

        Returns:
            list: List tuples, each an inversion.
        """
        inversions = []
        fb = Puzzle.flatten(board)
        for i in range(len(fb)):
            first = fb[i]
            for second in fb[i:]:
                if int(first) > int(second):
                    inversions.append((first, second))
            #print(f"{first}:  {fb[i:]}   |  {inversions}")
        #print(len(inversions))
        return inversions

    @staticmethod
    def empty_pos(board):
        return np.where(board == Puzzle.EMPTY)

    @staticmethod
    def flatten(board):
        """
        Flattens the game board into a 1D array, removing the empty space.

        Args:
            board (numpy.ndarray): Array representing the board state.

        Returns:
            list: 1D array of flattened board.
        """
        flat = board.flatten()
        return [i for i in flat if i != '_']

    @staticmethod
    def solvable(board):
        """
        Returns if the amount of inversions is even. If so, the game is solvable.

        NOTE: This does not apply to the initial state.

        Args:
            board (numpy.ndarray): Array representing the board state.

        Returns:
            bool: If the game is solvable.
        """
        if len(Puzzle.get_inversions(board)) % 2 == 0:
            return True
        return False

    @staticmethod
    def solved(board):
        return np.array_equal(board, Puzzle.GOAL)

    @staticmethod
    def get(board, position : tuple):
        return board[position][0]

    @staticmethod
    def get_move_position(board, move: Action):
        """
        Returns the location of the board piece that will move during the specified action.

        Args:
            move (Action): The action that will cause a piece to be moved.

        Raises:
            Exception: If move is not valid.

        Returns:
            numpy.ndarray: Location of piece to be moved to the empty position in form [y, x].
        """
        empty_pos = Puzzle.empty_pos(board)
        move_pos = None
        if move == Action.U:
            move_pos = (empty_pos[0] + 1, empty_pos[1])
        elif move == Action.D:
            move_pos = (empty_pos[0] - 1, empty_pos[1])
        elif move == Action.L:
            move_pos = (empty_pos[0], empty_pos[1] + 1)
        elif move == Action.R:
            move_pos = (empty_pos[0], empty_pos[1] - 1)
        else:
            raise Exception(f"ERROR: Move {move} is not a valid move.")

        return move_pos

    @staticmethod
    def move_result(board, move: Action):
        """
        Returns the board state after a move, but does not update the board.

        Args:
            move (Action): What direction to move a piece.

        Returns:
            numpy.ndarray: New board if piece was moved successfully.
        """
        if move not in Puzzle.possible_moves(board):
            raise Exception(f"ERROR: Can not move {move}. Current position: {Puzzle.pos_str(board)}")

        move_pos = Puzzle.get_move_position(board, move)
        moving_piece = Puzzle.get(board, move_pos)

        new_board = np.copy(board)
        new_board[Puzzle.empty_pos(board)] = moving_piece
        new_board[move_pos] = Puzzle.EMPTY

        return new_board

    @staticmethod
    def move_cost(board, move: Action):
        """
        Calculates the inversion cost of a move.

        Args:
            move (Action): Move to attempt.

        Returns:
            int: How many inversions will exist after the move.
        """
        empty_pos = Puzzle.empty_pos(board)
        move_pos = Puzzle.get_move_position(board, move)
        moving_piece = Puzzle.get(board, move_pos)

        new_board = np.copy(board)
        new_board[empty_pos] = moving_piece
        new_board[move_pos] = Puzzle.EMPTY

        return len(Puzzle.get_inversions(new_board))

    @staticmethod
    def pos_str(board):
        empty_pos = Puzzle.empty_pos(board)
        return [(l[0]) for l in empty_pos]

    @staticmethod
    def possible_moves(board):
        possible_moves = [Action.L, Action.R, Action.U, Action.D]

        empty_pos = Puzzle.empty_pos(board)
        if empty_pos[0] == 0:
            possible_moves.pop(possible_moves.index(Action.D))
        if empty_pos[0] == 2:
            possible_moves.pop(possible_moves.index(Action.U))
        if empty_pos[1] == 0:
            possible_moves.pop(possible_moves.index(Action.R))
        if empty_pos[1] == 2:
            possible_moves.pop(possible_moves.index(Action.L))

        return possible_moves

    @staticmethod
    def possible_states(board):
        """
        Returns all possible states after each move based on the current board state.
        """
        possible_moves = Puzzle.possible_moves(board)
        possible_states = []
        for move in possible_moves:
            move_pos = Puzzle.get_move_position(board, move)
            moving_piece = Puzzle.get(board, move_pos)

            empty_pos = Puzzle.empty_pos(board)
            new_board = np.copy(board)
            new_board[empty_pos] = moving_piece
            new_board[move_pos] = Puzzle.EMPTY

            solvable = Puzzle.solvable(new_board)
            if not solvable:
                continue
            possible_states.append(new_board)

        return possible_states

