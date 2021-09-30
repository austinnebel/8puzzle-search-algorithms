from enum import Enum
import numpy as np

class Action(Enum):
    L = 0
    R = 1
    U = 2
    D = 3

class BoardNode:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    EMPTY = "_"
    GOAL = np.array([['1', '2', '3'],
                     ['4', '5', '6'],
                     ['7', '8', '_']])

    def __init__(self, state : np.ndarray, parent = None, action = None, path_cost = 0):
        """
        Creates a Board node representing the result of action being applied to parent.

        Args:
            state (numpy.ndarray): Current state of the board.
            parent (BoardNode, optional): BoardNode representing the previous state of the board. Defaults to None.
            action (Action, optional): Action applied to parent that resulted in this node's state. Defaults to None.
            path_cost (int, optional): Cost of the action. Defaults to 0.
        """
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

        self.inversions = self._get_inversions()
        self.empty_pos = np.where(self.state == BoardNode.EMPTY)
        self.path_cost = len(self.inversions)
        self.solvable = True if len(self.inversions) % 2 == 0 else False
        self.solved = np.array_equal(self.state, BoardNode.GOAL)
        self.possible_moves = self._possible_moves()

    def get(self, position : tuple):
        return self.state[position][0]

    def get_move_position(self, move: Action):
        """
        Returns the location of the board piece that will move during the specified action.

        Args:
            move (Action): The action that will cause a piece to be moved.

        Raises:
            Exception: If move is not valid.

        Returns:
            numpy.ndarray: Location of piece to be moved to the empty position in form [y, x].
        """
        empty_pos = self.empty_pos
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

    def _get_inversions(self):
            """
            Returns the current amount of inversions.

            An inversion is when a larger number is before a smaller number.
            Ex. If the board state is [1, 2, 4, 8, _, 5, 6, 7, 3],
                then the inversions are (4, 3), (8, 5), (8, 6), (8, 3), (7, 3)

            If there are no inversions, the game is won. If there is an odd number

            Returns:
                list: List tuples, each an inversion.
            """
            inversions = []
            fb = self.flatten()
            for i in range(len(fb)):
                first = fb[i]
                for second in fb[i:]:
                    if int(first) > int(second):
                        inversions.append((first, second))
            return inversions

    def flatten(self):
        """
        Flattens the game board into a 1D array, removing the empty space.

        Returns:
            list: 1D array of flattened board.
        """
        flat = self.state.flatten()
        return [i for i in flat if i != '_']

    def move_result(self, move: Action):
            """
            Returns the board state after a move, but does not update the board.

            Args:
                move (Action): What direction to move a piece.

            Returns:
                numpy.ndarray: New board if piece was moved successfully.
            """
            if move not in self.possible_moves:
                raise Exception(f"ERROR: Can not move {move}. Current position: {self.empty_pos}")

            move_pos = self.get_move_position(move)
            moving_piece = self.get(move_pos)

            new_board = np.copy(self.state)
            new_board[self.empty_pos] = moving_piece
            new_board[move_pos] = BoardNode.EMPTY

            return new_board

    def _possible_moves(self):
        """
        Returns all possible moves based on the location of this node's empty slot.

        Returns:
            list: List of Action enums.
        """
        possible_moves = [Action.L, Action.R, Action.U, Action.D]

        if self.empty_pos[0] == 0:
            possible_moves.pop(possible_moves.index(Action.D))
        if self.empty_pos[0] == 2:
            possible_moves.pop(possible_moves.index(Action.U))
        if self.empty_pos[1] == 0:
            possible_moves.pop(possible_moves.index(Action.R))
        if self.empty_pos[1] == 2:
            possible_moves.pop(possible_moves.index(Action.L))

        return possible_moves

    def expand(self):
        """
        Returns all possible child nodes based on this node's board state.
        """
        children = []
        for move in self.possible_moves:
            move_pos = self.get_move_position(move)
            moving_piece = self.get(move_pos)

            # copy this node's state, and swap the empty position with the move position
            new_board = np.copy(self.state)
            new_board[self.empty_pos] = moving_piece
            new_board[move_pos] = BoardNode.EMPTY

            # create child node
            new_node = BoardNode(new_board, parent = self, action = move)

            # if new board state isn't solvable, don't continue
            if not new_node.solvable:
                print(f"Node {new_node} is not solvable. It has {len(new_node.inversions)} inversions.")
                continue

            # create a new BoardNode and append
            children.append(new_node)

        return children

    def tolist(self):
        return self.state.flatten()

    def tuple(self):
        return tuple(self.tolist())

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def __repr__(self):
        return f"<Node {self.tolist()}>"

    def __lt__(self, node):
        return self.state < node.state

    def __eq__(self, other):
        return isinstance(other, BoardNode) and np.array_equal(self.state, other.state)

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)
