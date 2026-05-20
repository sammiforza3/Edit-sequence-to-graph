# EDIT-sequence-to-graph

This project implements an algorithm to compute the minimum edit distance between a pattern and a path inside a directed acyclic graph (DAG).

The algorithm uses dynamic programming to build an edit-distance matrix and a backtracking matrix. The backtracking matrix is then used to reconstruct the path in the graph that is closest to the input pattern.

## Requirements

The code requires Python 3 and the following libraries:

```bash
pip install networkx matplotlib
```

## How to run

Run the program from the terminal with:

```bash
python main.py
```

If the Python file has a different name, replace `main.py` with the actual filename.

## What the program does

The program:

- defines a labelled directed acyclic graph;
- adds a dummy starting node `S0`;
- computes a topological ordering of the graph nodes;
- builds the edit-distance matrix;
- builds the backtracking matrix;
- reconstructs the path with minimum edit distance;
- prints the closest path, the closest string, and the final edit distance;
- displays a graphical representation of the graph.

## Toy examples

The program contains two toy examples.

### Toy Example 1

The first toy example uses the pattern:

```python
pattern = "CAC"
```

It runs the algorithm on a small labelled DAG and computes the path whose sequence has the minimum edit distance from the pattern.

### Toy Example 2

The second toy example uses the pattern:

```python
pattern = "ACTGTA"
```

It runs the same algorithm on a larger labelled DAG, showing that the implementation can be reused with different graphs and patterns.

## Output

For each toy example, the program prints:

- the graph structure after adding the dummy node `S0`;
- the topological ordering of the nodes;
- the edit-distance matrix;
- the backtracking matrix;
- the closest path in the graph;
- the string associated with that path;
- the final edit distance.

The program also opens a graphical visualization of the DAG using `networkx` and `matplotlib`.