import os
import time
import sys
import statistics
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

        # h function is the sum of the tile distance of each tile from its goal position
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
        print("Using A* with Euclidian distance heuristic.")

        def subtract_boards(node):
            node_int = np.char.replace(node.state, '_', '9').astype(int)
            goal_int = np.char.replace(node.GOAL, '_', '9').astype(int)
            sub = np.linalg.norm(goal_int - node_int)
            return sub

        # h function is the sum of the  distance of each tile from its goal position
        return hstar.search(root, subtract_boards)

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
        print("ERROR: Not enough arguments. Usage: python main.py [file path OR folder] [algorithm]")
        exit(1)

    file = args[1]
    alg_name = args[2].lower()

    try:
        alg = getattr(Algorithms, alg_name)
    except AttributeError:
        available_algs = [method_name for method_name in dir(Algorithms) if "__" not in method_name]
        print(f"Algorithm '{alg_name}' is not valid. Available algorithms: {available_algs}")
        exit(2)

    if os.path.isdir(file):
        print(f"Processing folder '{file}' with algorithm '{alg_name}'")
        results = []
        visit_counts = []
        times = []
        for f in os.listdir(file):
            print(f"Processing file '{f}'")
            result, visit_count, time = start(os.path.join(file, f), alg)
            results.append(result)
            times.append(time)
            visit_counts.append(visit_count)
        print("----------------------------------------------------")
        print(f"Average run time: {statistics.mean(times)}")
        print(f"Average explored nodes: {statistics.mean(visit_counts)}")
        return

    start(file, alg)

def start(file, algorithm):

    board = initialize(file)

    start = time.time()
    result, visit_count = algorithm(board)
    if result:
        print(f"Found goal  : {result}.")
        path = np.array(result.path())
        #print(f"Path: \n{path}")
        print(f"Path Length : {len(path)}")
        print(f"Moves       : {'-'.join([n.action.name for n in path[1:]])}")
    else:
        print("Goal not found.")

    exec_time = time.time() - start
    print(f"Execution time: {exec_time} seconds.\n")

    return result, visit_count, exec_time


if __name__ == "__main__":
    main()