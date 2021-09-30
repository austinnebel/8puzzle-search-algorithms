import sys
from puzzle import BoardNode

def depth_limited_search(root_node : BoardNode, limit=50):
    """[Figure 3.17]"""

    def recursive_dls(node, limit):
        if node.solved:
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand():
                result = recursive_dls(child, limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None

    # Body of depth_limited_search:
    return recursive_dls(root_node, limit)

def search(problem):
    """Iterative deepening DFS"""
    for depth in range(sys.maxsize):
        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result