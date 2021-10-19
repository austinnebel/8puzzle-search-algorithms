import time
from collections import deque

def search(root_node):
    """BFS search algorithm."""

    node = root_node
    if node.solved:
        return node, 1

    fringe = deque([node])
    fringe_set = set([node.hashable()])
    visited = set([node.hashable()])
    visit_count = 0
    created_count = 1

    s = time.time()
    while fringe:
        node = fringe.popleft()
        fringe_set.remove(node.hashable())
        visit_count += 1

        if time.time() - s > 15*60:
            print(f"ERROR: Timed out after {time.time() - s} minutes.")
            print(f"BFS nodes: Created: {created_count} Visited: {visit_count}")
            exit(3)

        children = node.expand()
        for child in children:

            if child.solved:
                print(f"BFS nodes: Created: {created_count}  Visited: {visit_count}")
                return child, visit_count

            child_hashable = child.hashable()
            if not child_hashable in visited and not child_hashable in fringe_set:
                fringe.append(child)
                fringe_set.add(child.hashable())
                visited.add(child_hashable)
                created_count += 1

    print(f"BFS nodes: Created: {created_count}  Visited: {visit_count}")
    return None, visit_count