import time
import sys
import numpy as np

from puzzle.node import BoardNode
import algorithms.bfs as bfs
import algorithms.ids as ids
import algorithms.hstar as hstar

class Algorithms:

    @staticmethod
    def bfs(root):
        print("Using BFS.")
        return bfs.search(root)

    @staticmethod
    def ids(root):
        print("Using IDS.")
        return ids.search(root)

    @staticmethod
    def h1(root):
        print("Using A* with misplaced title heuristic.")
        # h function is the count of all tiles not in the correct location
        return hstar.search(root, lambda n: (n.state != n.GOAL).sum())

    @staticmethod
    def h2(root):
        print("Using A* with Manhattan distance heuristic.")

        # h function is the sum of the distance of each tile from its goal position
        def distance(node):
            total = 0
            for row in range(3):
                for col in range(3):
                    cur_point = np.array([row, col])
                    goal_point = np.where(node.state[(row, col)] == BoardNode.GOAL)
                    dist = np.sum(np.abs(cur_point - np.array(list(goal_point)).flatten()))
                    #print(np.sum(np.abs(cur_point - np.array(list(goal_point)).flatten())))
                    total += dist

            return total

        return hstar.search(root, distance)

    @staticmethod
    def h3(root):
        print("Using A* with one more heuristic.")
        return hstar.search(root)

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

    """board = np.array([['1', '2', '3'],
                     ['4', '6', '8'],
                     ['7', '5', '_']])"""

    return BoardNode(board)

def main():

    args = sys.argv

    if len(args) != 3:
        print("ERROR: Not enough arguments. Usage: python main.py [file path] [algorithm]")
        exit(1)

    file = args[1]
    alg_name = args[2].lower()

    try:
        alg = getattr(Algorithms, alg_name)
    except AttributeError:
        available_algs = [method_name for method_name in dir(Algorithms) if "__" not in method_name]
        print(f"Algorithm '{alg_name}' is not valid. Available algorithms: {available_algs}")
        exit(2)

    board = initialize(file)

    start = time.time()
    finish = alg(board)
    if finish:
        print("Found goal.")
        path = np.array(finish.path())
        print(f"Path: \n{path}")
        print(f"Path Length: \n{len(path)}")
    print(f"Execution time: {time.time()-start} seconds.")


if __name__ == "__main__":

    main()