# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import os
import csv
import sys


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


class SearchLogger:
    """
    Automated CSV Trace Logger conforming to Assignment 01 Specification:
    iteration, expanded_state, parent, action, generated_successors,
    frontier_before, frontier_after, explored, g, h, f
    """
    def __init__(self, algo_name, problem):
        self.algo_name = algo_name
        self.problem = problem
        self.iteration = 0
        self.rows = []
        self.evidence_dir = "evidence"
        os.makedirs(self.evidence_dir, exist_ok=True)

        # Detect layout/problem name from CLI args or problem attributes
        layout_name = None
        for idx, arg in enumerate(sys.argv):
            if arg == "-l" and idx + 1 < len(sys.argv):
                layout_name = sys.argv[idx + 1]
                break
        if not layout_name:
            layout_name = problem.__class__.__name__

        self.filename = os.path.join(self.evidence_dir, f"{algo_name}_{layout_name}.csv")
        self.trace_filename = os.path.join(self.evidence_dir, f"{algo_name}_trace.csv")

    def log(self, expanded_state, parent, action, generated_successors,
            frontier_before, frontier_after, explored_set, g=0.0, h=0.0, f=0.0):
        self.iteration += 1
        
        # Format successors and frontier for clean CSV storage
        succ_repr = [s[0] for s in generated_successors] if generated_successors else []
        front_b_repr = list(frontier_before) if len(frontier_before) <= 15 else f"{len(frontier_before)} items"
        front_a_repr = list(frontier_after) if len(frontier_after) <= 15 else f"{len(frontier_after)} items"
        exp_repr = list(explored_set) if len(explored_set) <= 15 else f"{len(explored_set)} items"

        row = [
            self.iteration,
            str(expanded_state),
            str(parent) if parent is not None else "START",
            str(action) if action is not None else "START",
            str(succ_repr),
            str(front_b_repr),
            str(front_a_repr),
            str(exp_repr),
            round(float(g), 2),
            round(float(h), 2),
            round(float(f), 2)
        ]
        self.rows.append(row)

    def write(self):
        header = [
            "iteration", "expanded_state", "parent", "action",
            "generated_successors", "frontier_before", "frontier_after",
            "explored", "g", "h", "f"
        ]
        for path in {self.filename, self.trace_filename}:
            try:
                with open(path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerows(self.rows)
            except Exception:
                pass


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.
    Technical Requirements:
    - Use a LIFO Stack from util.py as frontier.
    - Strict graph search: maintain an explicit explored set.
    - Return a valid list of actions.
    - Follow mandatory successor expansion order: North -> East -> South -> West.
    """
    logger = SearchLogger("dfs", problem)
    start_state = problem.getStartState()
    frontier = util.Stack()
    
    # Store tuples: (state, actions_to_here, parent_state, action_taken)
    frontier.push((start_state, [], None, None))
    explored = set()

    DIR_ORDER = {'North': 0, 'East': 1, 'South': 2, 'West': 3}

    while not frontier.isEmpty():
        frontier_before = [item[0] for item in frontier.list]
        state, actions, parent, action = frontier.pop()

        if problem.isGoalState(state):
            logger.log(state, parent, action, [], frontier_before,
                       [item[0] for item in frontier.list], explored, g=len(actions), h=0.0, f=len(actions))
            logger.write()
            return actions

        if state not in explored:
            explored.add(state)
            successors = problem.getSuccessors(state)

            for next_state, next_action, cost in successors:
                if next_state not in explored:
                    frontier.push((next_state, actions + [next_action], state, next_action))

            frontier_after = [item[0] for item in frontier.list]
            logger.log(state, parent, action, successors, frontier_before,
                       frontier_after, explored, g=len(actions), h=0.0, f=len(actions))

    logger.write()
    return []


def breadthFirstSearch(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    Technical Requirements:
    - Use a FIFO Queue from util.py as fringe/frontier.
    - Guarantee shallowest/optimal path on unweighted graphs.
    - Avoid re-enqueuing states that are already present in frontier or explored set.
    """
    logger = SearchLogger("bfs", problem)
    start_state = problem.getStartState()
    frontier = util.Queue()
    frontier.push((start_state, [], None, None))

    # Keep track of states present in frontier or already explored
    seen = {start_state}
    explored = set()

    while not frontier.isEmpty():
        frontier_before = [item[0] for item in frontier.list]
        state, actions, parent, action = frontier.pop()

        if problem.isGoalState(state):
            logger.log(state, parent, action, [], frontier_before,
                       [item[0] for item in frontier.list], explored, g=len(actions), h=0.0, f=len(actions))
            logger.write()
            return actions

        explored.add(state)
        successors = problem.getSuccessors(state)

        for next_state, next_action, cost in successors:
            if next_state not in seen:
                seen.add(next_state)
                frontier.push((next_state, actions + [next_action], state, next_action))

        frontier_after = [item[0] for item in frontier.list]
        logger.log(state, parent, action, successors, frontier_before,
                   frontier_after, explored, g=len(actions), h=0.0, f=len(actions))

    logger.write()
    return []


def uniformCostSearch(problem: SearchProblem):
    """
    Search the node of least total cost first.
    Technical Requirements:
    - Use a PriorityQueue from util.py ordered by accumulated path cost g(n).
    - Varying step costs support.
    - Handle frontier updates via PriorityQueue.update when cheaper path is found.
    """
    logger = SearchLogger("ucs", problem)
    start_state = problem.getStartState()
    frontier = util.PriorityQueue()
    frontier.push(start_state, 0.0)

    explored = set()
    best_g = {start_state: 0.0}
    path_to = {start_state: []}
    parent_map = {start_state: (None, None)}

    while not frontier.isEmpty():
        frontier_before = [entry[2] for entry in frontier.heap]
        state = frontier.pop()

        actions = path_to[state]
        parent, action = parent_map[state]
        current_g = best_g[state]

        if problem.isGoalState(state):
            logger.log(state, parent, action, [], frontier_before,
                       [entry[2] for entry in frontier.heap], explored, g=current_g, h=0.0, f=current_g)
            logger.write()
            return actions

        if state in explored:
            continue
        explored.add(state)

        successors = problem.getSuccessors(state)
        for next_state, next_action, step_cost in successors:
            if next_state in explored:
                continue
            new_g = current_g + step_cost
            if next_state not in best_g or new_g < best_g[next_state]:
                best_g[next_state] = new_g
                path_to[next_state] = actions + [next_action]
                parent_map[next_state] = (state, next_action)
                frontier.update(next_state, new_g)

        frontier_after = [entry[2] for entry in frontier.heap]
        logger.log(state, parent, action, successors, frontier_before,
                   frontier_after, explored, g=current_g, h=0.0, f=current_g)

    logger.write()
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem. This heuristic is trivial.
    """
    return 0


def greedyBestFirstSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Greedy Best-First Search (alias: gbfs).
    Technical Requirements:
    - Use a PriorityQueue ordered strictly by heuristic value h(n).
    - Support dynamic command-line heuristic parameter passing.
    """
    logger = SearchLogger("gbfs", problem)
    start_state = problem.getStartState()
    frontier = util.PriorityQueue()
    start_h = heuristic(start_state, problem)
    frontier.push(start_state, start_h)

    explored = set()
    best_h = {start_state: start_h}
    cost_to = {start_state: 0.0}
    path_to = {start_state: []}
    parent_map = {start_state: (None, None)}

    while not frontier.isEmpty():
        frontier_before = [entry[2] for entry in frontier.heap]
        state = frontier.pop()

        actions = path_to[state]
        parent, action = parent_map[state]
        current_g = cost_to[state]
        current_h = best_h.get(state, heuristic(state, problem))

        if problem.isGoalState(state):
            logger.log(state, parent, action, [], frontier_before,
                       [entry[2] for entry in frontier.heap], explored, g=current_g, h=current_h, f=current_h)
            logger.write()
            return actions

        if state in explored:
            continue
        explored.add(state)

        successors = problem.getSuccessors(state)
        for next_state, next_action, step_cost in successors:
            if next_state in explored:
                continue
            next_h = heuristic(next_state, problem)
            if next_state not in path_to or next_h < best_h.get(next_state, float("inf")):
                best_h[next_state] = next_h
                cost_to[next_state] = current_g + step_cost
                path_to[next_state] = actions + [next_action]
                parent_map[next_state] = (state, next_action)
                frontier.update(next_state, next_h)

        frontier_after = [entry[2] for entry in frontier.heap]
        logger.log(state, parent, action, successors, frontier_before,
                   frontier_after, explored, g=current_g, h=current_h, f=current_h)

    logger.write()
    return []


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    A* Search (alias: astar).
    Technical Requirements:
    - Use a PriorityQueue ordered by evaluation function f(n) = g(n) + h(n).
    - Verify optimality with admissible and consistent heuristic.
    - Priority updates when cheaper g(n) path is found.
    """
    logger = SearchLogger("astar", problem)
    start_state = problem.getStartState()
    frontier = util.PriorityQueue()
    start_h = heuristic(start_state, problem)
    frontier.push(start_state, start_h)

    explored = set()
    best_g = {start_state: 0.0}
    path_to = {start_state: []}
    parent_map = {start_state: (None, None)}

    while not frontier.isEmpty():
        frontier_before = [entry[2] for entry in frontier.heap]
        state = frontier.pop()

        actions = path_to[state]
        parent, action = parent_map[state]
        current_g = best_g[state]
        current_h = heuristic(state, problem)
        current_f = current_g + current_h

        if problem.isGoalState(state):
            logger.log(state, parent, action, [], frontier_before,
                       [entry[2] for entry in frontier.heap], explored, g=current_g, h=current_h, f=current_f)
            logger.write()
            return actions

        if state in explored:
            continue
        explored.add(state)

        successors = problem.getSuccessors(state)
        for next_state, next_action, step_cost in successors:
            if next_state in explored:
                continue
            new_g = current_g + step_cost
            if next_state not in best_g or new_g < best_g[next_state]:
                best_g[next_state] = new_g
                path_to[next_state] = actions + [next_action]
                parent_map[next_state] = (state, next_action)
                next_f = new_g + heuristic(next_state, problem)
                frontier.update(next_state, next_f)

        frontier_after = [entry[2] for entry in frontier.heap]
        logger.log(state, parent, action, successors, frontier_before,
                   frontier_after, explored, g=current_g, h=current_h, f=current_f)

    logger.write()
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
gbfs = greedyBestFirstSearch
