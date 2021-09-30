from collections import deque
from puzzle import BoardNode



def search(root_node : BoardNode):
    """[Figure 3.11]
    Note that this function can be implemented in a
    single line as below:
    return graph_search(problem, FIFOQueue())
    """
    node = root_node
    if node.solved:
        return node

    fringe = deque([node])
    visited = set([node.hashable()])

    while fringe:

        node = fringe.popleft()
        children = node.expand()
        print(node)

        for child in children:

            if child.solved:
                return child

            child_hashable = child.hashable()
            if not child_hashable in visited and not child_hashable in fringe:
                fringe.append(child)
                visited.add(child_hashable)

    return None