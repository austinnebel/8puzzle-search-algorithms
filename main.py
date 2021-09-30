import sys
import numpy as np

from puzzle import Puzzle

class Algorithms:

    @staticmethod
    def BFS(puzzle):
        print(bfs.search(puzzle))

    def IDS(self):
        pass

    def h1(self):
        pass

    def h2(self):
        pass

    def h3(self):
        pass


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

    board = Puzzle.initialize(file)

    alg(board)

if __name__ == "__main__":
    import algorithms.bfs as bfs
    main()