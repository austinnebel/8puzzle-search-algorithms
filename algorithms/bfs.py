from collections import deque
import numpy as np
import time
from puzzle import BoardNode

def search(root_node : BoardNode):
    """[Figure 3.11]
    Note that this function can be implemented in a
    single line as below:
    return graph_search(problem, FIFOQueue())
    """
    start = time.time()

    node = root_node
    if root_node.solved:
        return node

    # who is waiting for a visit
    visit_queue = deque([node])
    # who has been visited already
    visited = deque([node])
    while visit_queue:
        node = visit_queue.popleft()

        children = node.expand()
        visited.append(node)
        for child in children:

            if child == child.parent:
                continue

            if child not in visited and not child in visit_queue:
                    if child.solved:
                        return child

                    visit_queue.append(child)

            if time.time()-start > 15*60:
                print(f"Timed out after 15 minutes.")
                return None

    print(f"Not found after {time.time()-start} seconds.")
    return None
