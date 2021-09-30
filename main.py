import time
from puzzle.node import BoardNode
import sys
import numpy as np

from puzzle import Puzzle

class Algorithms:

    @staticmethod
    def BFS(root):
        return bfs.search(root)

    def IDS(self):
        pass

    def h1(self):
        pass

    def h2(self):
        pass

    def h3(self):
        pass

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
    alg_name = args[2]

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
        print(f"Path: \n{np.array(finish.path())}")
    print(f"Execution time: {time.time()-start} seconds.")


if __name__ == "__main__":
    import algorithms.bfs as bfs
    main()