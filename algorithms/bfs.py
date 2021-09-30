from collections import deque
import numpy as np
import time
from puzzle import Puzzle, BoardNode

def search(board):
    """[Figure 3.11]
    Note that this function can be implemented in a
    single line as below:
    return graph_search(problem, FIFOQueue())
    """
    start = time.time()

    node = BoardNode(board)
    if Puzzle.solved(node.state):
        return node

    # who is waiting for a visit
    visit_queue = deque([node])
    # who has been visited already (unique only)
    visited = set()

    while visit_queue:
        node = visit_queue.popleft()

        visited.add(node.tuple())
        children = node.expand()
        for child in children:

            if child == child.parent:
                continue

            if child.tuple() not in visited:
                if not np.any([child == f for f in visit_queue]):

                    if Puzzle.solved(child.state):
                        print(len(visited))
                        print(f"Found in {time.time()-start} seconds.")
                        return child

                    visit_queue.append(child)

    print(f"Not found after {time.time()-start} seconds.")
    return None
