import numpy as np
from .puzzle import Puzzle, Action

class BoardNode:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent = None, action = None, path_cost = 0):
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

    def expand(self):
        """
        List the nodes reachable in one step from this node.

        Gets a list of possible moves based on this node's board state,
        and creates a child node with each of them.
        """
        return [self.child_node(self.state, action)
                for action in Puzzle.possible_moves(self.state)
                if action is not None]

    def child_node(self, board, move : Action):
        """
        Creates a child node of this one based on the resulting board of the specified move.

        If a the specified move creates an impossible game state, returns none.
        """
        next_board_state = Puzzle.move_result(board, move)
        move_cost = Puzzle.move_cost(board, move)

        if np.any([np.array_equal(next_board_state, s) for s in Puzzle.possible_states(board)]):
            next_node = BoardNode(next_board_state, parent = self, action = move, path_cost = move_cost)
            return next_node
        return None

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
