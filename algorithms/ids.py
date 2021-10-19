import time
import sys
from collections import deque

visit_count = 0
created_count = 1
s = 0
def depth_limited_search(root_node, depth):
    fringe = deque([root_node]) # LIFO
    global visit_count
    global created_count
    global s

    result = None
    while fringe:
        node = fringe.pop()
        visit_count += 1
        if node.solved:
            return node
        if time.time() - s > 15*60:
            print(f"ERROR: Timed out after {(time.time() - s)/60} minutes.")
            exit(3)

        if node.depth >= depth:
            result =  "cutoff"
        elif not node.hashable() in [n.hashable() for n in node.path()[:-1]]:
            for child in node.expand():
                if node.parent is not None and child.hashable() == node.parent.hashable():
                    continue
                fringe.append(child)
                created_count += 1

    return result

def search(root):
    global visit_count
    global created_count
    global s
    s = time.time()

    visit_count = 0
    created_count = 1
    for depth in range(sys.maxsize):
        result = depth_limited_search(root, depth)
        if result != "cutoff":
            print(f"IDS nodes: Created: {created_count} Visited: {visit_count}")
            return result, visit_count
        depth *=2
    print(f"IDS nodes: Created: {created_count} Visited: {visit_count}")
    return result, visit_count