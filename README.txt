========================================================================
ARTIFICIAL INTELLIGENCE (AI2002) - ASSIGNMENT 01
PACMAN SEARCH PROJECT & HEURISTIC OPTIMIZATION
========================================================================

1. SYSTEM & ENVIRONMENT SPECIFICATIONS
------------------------------------------------------------------------
Operating System: Windows 11 / x86_64
Python Version: Python 3.10+ / Python 3.12 (Standard CPython)
Required Packages: Built-in standard library (sys, os, csv, time, heapq, itertools)
Optional Visualization: matplotlib, numpy, Pillow (for PNG chart generation)
Autograder Score: 26 / 25 (100% Passing + Extra Credit)


2. PROJECT DIRECTORY STRUCTURE
------------------------------------------------------------------------
Search-AIProject/
├── search.py                # Core search algorithms (DFS, BFS, UCS, GBFS, A*) + CSV Logger
├── searchAgents.py          # State space models (CornersProblem, FoodSearchProblem) & Heuristics
├── pacman.py                # Game loop controller and CLI runner (DO NOT MODIFY)
├── game.py                  # Core engine, agents, and directions (DO NOT MODIFY)
├── util.py                  # Data structures: Stack, Queue, PriorityQueue (DO NOT MODIFY)
├── layout.py                # Maze loader (DO NOT MODIFY)
├── autograder.py            # Automated test suite
├── README.txt               # System specs, run commands, and overview
├── EXPLANATION.md           # In-depth architectural & theoretical explanation file
├── layouts/                 # Maze layout definitions
│   ├── Search.lay           # Custom maze with deceptive traps
│   ├── 21I1234Search.lay    # Custom maze layout (Student ID alias)
│   ├── tinyMaze.lay, mediumMaze.lay, bigMaze.lay, etc.
│   ├── mediumDenselyMaze.lay, stayEastSearch.lay
├── evidence/                # Automated CSV trace logs for all runs
│   ├── *.csv                # State-by-state execution logs (11 mandatory columns)
│   └── screenshots/         # Solution visualizations (.png and .txt)


3. VERIFICATION & RUN COMMANDS
------------------------------------------------------------------------
To run the automated grader across all questions:
    python autograder.py

To run individual questions on the autograder:
    python autograder.py -q q1   # Depth-First Search (DFS)
    python autograder.py -q q2   # Breadth-First Search (BFS)
    python autograder.py -q q3   # Uniform Cost Search (UCS)
    python autograder.py -q q4   # A* Search
    python autograder.py -q q5   # CornersProblem State Space
    python autograder.py -q q6   # cornersHeuristic (Admissible & Consistent)
    python autograder.py -q q7   # foodHeuristic (Minimum Spanning Tree / Bottleneck)
    python autograder.py -q q8   # ClosestDotSearchAgent / AnyFoodSearchProblem

------------------------------------------------------------------------
Interactive Graphical & Headless Pacman Commands:
------------------------------------------------------------------------

[Task 1: DFS]
    python pacman.py -l tinyMaze -p SearchAgent -a fn=dfs
    python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs
    python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=dfs

[Task 2: BFS]
    python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
    python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=bfs

[Task 3: UCS]
    python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
    python pacman.py -l mediumDenselyMaze -p SearchAgent -a fn=ucs
    python pacman.py -l stayEastSearch -p SearchAgent -a fn=ucs

[Task 4: GBFS]
    python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic
    python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=gbfs,heuristic=euclideanHeuristic

[Task 5: A* Search]
    python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=nullHeuristic
    python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

[Task 6: Multi-Goal State Space (Corners Problem)]
    python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
    python pacman.py -l mediumCorners -p AStarCornersAgent -z .5

[Task 7: Eating All Food Dots & Nearest Food Search]
    python pacman.py -l trickySearch -p AStarFoodSearchAgent
    python pacman.py -l bigSearch -p ClosestDotSearchAgent

[Task 8: Custom Maze Experiments (Search.lay)]
    python pacman.py -l Search -p SearchAgent -a fn=dfs
    python pacman.py -l Search -p SearchAgent -a fn=bfs
    python pacman.py -l Search -p SearchAgent -a fn=ucs
    python pacman.py -l Search -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic
    python pacman.py -l Search -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic


4. CUSTOM MAZE EXPERIMENTAL RESULTS (Search.lay)
------------------------------------------------------------------------
Layout Dimensions: 25 x 13
Start State: (23, 6) | Goal State: (1, 1)

Algorithm | Path Cost | Nodes Expanded | Optimal? | Behavior Summary
----------|-----------|----------------|----------|-----------------------------------------
DFS       |    37     |      144       |   Yes*   | Dives down deceptive dead-end alleys first
BFS       |    37     |       77       |   Yes    | Explores shallowest frontiers uniformly
UCS       |    37     |       77       |   Yes    | Identical to BFS under uniform edge costs
GBFS      |    37     |      144       |   Yes*   | Trapped by low h(n) into dead-end corridor
A*        |    37     |       71       |   Yes    | Most efficient! Prunes trap using g(n)+h(n)

*Key finding: GBFS expands 144 nodes due to the deceptive Manhattan trap,
whereas A* expands only 71 nodes (a >50% reduction in node expansions)!


5. AUTOMATED CSV TRACE LOGGING
------------------------------------------------------------------------
Trace logs are automatically recorded to `evidence/` on every execution with
the required columns:
    iteration, expanded_state, parent, action, generated_successors,
    frontier_before, frontier_after, explored, g, h, f
========================================================================
