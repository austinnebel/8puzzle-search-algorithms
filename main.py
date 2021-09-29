import sys
from enum import Enum

import numpy as np


class Action:
    L = 0
    R = 1
    U = 2
    D = 3

class Puzzle:

    def __init__(self, init_state):
        """
        Initializes a 3x3 puzzle board.

        Args:
            init_state (list[string]): String list of initial board state, from top-left to bottom-right.
        """
        self.board = np.empty((3,3), dtype=str)
        self.board[0] = init_state[:3]
        self.board[1] = init_state[3:6]
        self.board[2] = init_state[6:]
        print(f"Initialized board:\n{self.board}")


class Algorithms:

    def BFS(self):
        pass

    def IDS(self):
        pass

    def h1(self):
        pass

    def h2(self):
        pass

    def h3(self):
        pass

def parse_puzzle(pfile):
    f = open(pfile, "r")
    plist = []
    for s in f.readlines():
        plist.extend(s.split())
    return plist

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

    s = parse_puzzle(file)
    print(f"Parsed puzzle from file: {s}")

    p = Puzzle(s)
    alg(p)

if __name__ == "__main__":
    main()