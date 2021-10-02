# Lab 1

## Requirements

-   pipenv
-   python 3.8

## Installation

-   Run the command `pipenv install` in this directory to install dependencies.
    -   numpy is the only dependency.

## How to Run

The `main.py` module is the only python file you need to run.

To use it, execute `python main.py [input file OR folder] [algorithm]`

Available algorithms are: BFS, IDS, H1, H2, H3.

-   The algorithms are not case sensitive.

After you run `main.py`, you should see output similar to the following:

```bash
❯ python main.py Part2/Part2/S15.txt bfs
Initialized board:
[['6' '4' '7']
 ['8' '5' '_']
 ['3' '2' '1']]
Using BFS.
BFS generated nodes: Created: 181439  Visited: 181379
Found goal  : <Node ['1' '2' '3' '4' '5' '6' '7' '8' '_']>.
Path Length : 32
Moves       : R-R-U-L-D-D-L-U-U-R-D-D-R-U-U-L-D-L-D-R-R-U-L-L-D-R-R-U-U-L-L
Execution time: 387.73353099823 seconds.
```

If the program is not solvable, it will print out the nodes that caused the unsolvability like so:

```bash
❯ python main.py Part2/Part2/S5.txt bfs
Initialized board:
[['2' '5' '3']
 ['4' '_' '7']
 ['8' '6' '1']]
Using BFS.
Node <Node ['2' '5' '3' '4' '7' '_' '8' '6' '1']> is not solvable. It has 11 inversions.
Node <Node ['2' '5' '3' '_' '4' '7' '8' '6' '1']> is not solvable. It has 11 inversions.
Node <Node ['2' '5' '3' '4' '6' '7' '8' '_' '1']> is not solvable. It has 9 inversions.
Node <Node ['2' '_' '3' '4' '5' '7' '8' '6' '1']> is not solvable. It has 9 inversions.
BFS visited nodes: Created: 1  Fringe: 1
Goal not found.
Execution time: 0.0013818740844726562 seconds.
```

In the event that the algorithm times out after 15 minutes, you will see output like so:

```bash
❯ python main.py Part2/Part2/S5.txt bfs
Initialized board:
[['2' '5' '3']
 ['4' '_' '7']
 ['8' '6' '1']]
Using BFS.
ERROR: Timed out after 15 minutes.
```

## References

Elements of algorithms.bfs, algorithms.hstar, algorithms.ids, and puzzle.node were referenced and heavily modified from [this repository.](https://github.com/aimacode/aima-python/blob/master/search.py)
