
from utils import expand, Node, PriorityQueue, Solution


def best_first(problem, f, max_steps=100, printer=None):

    n = Node(problem.initial)
    frontier = PriorityQueue(f)
    reached = dict()
    solution = None

    # initialization prints
    if printer is not None:
        printer(0, problem, frontier, reached, None, solution)

    reached[n.state] = n.path_cost    
    frontier.push(n)
    
    if printer is not None:
        printer(1, problem, frontier, reached, None, solution)

    n_iter = 2
    while len(frontier) > 0 and (n_iter - 2) < max_steps:

        n = frontier.pop()
        if problem.is_goal(n.state):
            solution = Solution(n)

            # 'solution found' print
            if printer is not None:
                printer(n_iter, problem, frontier, reached, n, solution)

            return solution

        for child in expand(problem, n):
            if child.state not in reached or child.path_cost < reached[child.state]:
                reached[child.state] = child.path_cost
                frontier.push(child)

        # 'after expansion' print
        if printer is not None:
            printer(n_iter, problem, frontier, reached, n, solution)

        n_iter += 1

    return None



def breadth_first(problem, max_steps=100, printer=None):

    n = Node(problem.initial)
    
    frontier = list() # frontier here is implemented as a list
    reached = set()
    solution = None

    # initialization prints
    if printer is not None:
        printer(0, problem, frontier, reached, None, solution)

    if problem.is_goal(n.state):
        solution = Solution(n)
                
        # 'solution found' print
        if printer is not None:
            printer(1, problem, frontier, reached, n, solution)

        return solution

    reached.add(n.state)
    frontier.append(n)
    
    if printer is not None:
        printer(1, problem, frontier, reached, None, solution)

    n_iter = 2
    while len(frontier) > 0 and (n_iter - 2) < max_steps:

        n = frontier.pop(0)
        for child in expand(problem, n):

            if problem.is_goal(child.state):
                solution = Solution(child)
                
                # 'solution found' print
                if printer is not None:
                    printer(n_iter, problem, frontier, reached, n, solution)

                return solution
            
            if child.state not in reached:
                reached.add(child.state)
                frontier.append(child)

        # 'after expansion' print
        if printer is not None:
            printer(n_iter, problem, frontier, reached, n, solution)

        n_iter += 1

    return None

def depth_first(problem, max_steps=100, printer=None):

    n = Node(problem.initial)
    
    frontier = list() # frontier here is implemented as a list
    reached = set()
    solution = None

    # initialization prints
    if printer is not None:
        printer(0, problem, frontier, reached, None, solution)

    if problem.is_goal(n.state):
        solution = Solution(n)
                
        # 'solution found' print
        if printer is not None:
            printer(1, problem, frontier, reached, n, solution)

        return solution

    reached.add(n.state)
    frontier.append(n)
    
    if printer is not None:
        printer(1, problem, frontier, reached, None, solution)

    n_iter = 2
    while len(frontier) > 0 and (n_iter - 2) < max_steps:

        n = frontier.pop()
        for child in expand(problem, n):

            if problem.is_goal(child.state):
                solution = Solution(child)
                
                # 'solution found' print
                if printer is not None:
                    printer(n_iter, problem, frontier, reached, n, solution)

                return solution
            
            if child.state not in reached:
                reached.add(child.state)
                frontier.append(child)

        # 'after expansion' print
        if printer is not None:
            printer(n_iter, problem, frontier, reached, n, solution)

        n_iter += 1

    return None


if __name__ == '__main__':

    import exercises
    from printers import cli_printer, pyplot_printer, debug_printer

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('alg', type=str,
                        help="Algorithm")

    parser.add_argument('--problem', type=str,
                        help="Problem",
                        default="weighted1")

    parser.add_argument('--seed', type=int,
                        help="Random seed number",
                        default=666)

    args = parser.parse_args()

    if args.problem.startswith("grid"):
        try:
            _, w, h, p_edge = args.problem.split("-")
        except ValueError:
            w, h, p_edge = 4, 3, 0.8

        problem = exercises.random_grid_problem(int(w), int(h), p_edge=float(p_edge), seed=args.seed)

    elif args.problem in exercises.named_exercises:        
        problem = exercises.named_exercises[args.problem]
    
    #printer = cli_printer     # uncomment for a command line interface printer
    printer = pyplot_printer     # uncomment for a graphical (pyplot-based) printer
    #printer = debug_printer

    # path cost (incr. state name in case of tie)
    no_heuristic = lambda node : (node.path_cost, node.state)

    # manhattan distance (incr. state name in case of tie)
    manhattan = lambda p1, p2 : abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    l1_to_closest_goal = lambda n, p : min(manhattan(problem.positions[n.state], problem.positions[g])
                            for g in problem.goals)
    heuristic_only = lambda node : (l1_to_closest_goal(node, problem), node.state)

    # both path cost and manhattan distance (incr. state name in case of tie)
    both = lambda node : (node.path_cost + l1_to_closest_goal(node, problem), node.state)
        
    if args.alg == 'bfs':
        breadth_first(problem, printer=printer, max_steps=100)
    elif args.alg == 'dfs':        
        depth_first(problem, printer=printer, max_steps=100)
    elif args.alg == 'ucs':
        best_first(problem, no_heuristic, printer=printer, max_steps=100)
    elif args.alg == 'greedy':
        best_first(problem, heuristic_only, printer=printer, max_steps=100)
    elif args.alg == 'astar':
        best_first(problem, both, printer=printer, max_steps=100)
    else:
        raise NotImplementedError(f"Algorithm {args.alg} not implemented.")


