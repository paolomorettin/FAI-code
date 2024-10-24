

import matplotlib.pyplot as plt
import networkx as nx
import os
from shutil import rmtree
from utils import Solution

def debug_printer(it, problem, frontier, reached, curr, solution):
    cli_printer(it, problem, frontier, reached, curr, solution, interactive=False)
    pyplot_printer(it, problem, frontier, reached, curr, solution, interactive=False)



def cli_printer(it, problem, frontier, reached, curr, solution, interactive=True):
    lse = '-' if curr is None else curr.state
    sol = '-' if solution is None else solution
    print(f"\niteration: {it} | last state expanded: {lse} | solution: {sol}")
    print(f"\tfrontier:")
    for n in frontier:
        print(f"\t\t{n}")
    print(f"\treached:\n\t\t{reached}")
    
    if interactive: input() # wait for key press


scale = 1.0
fig_h = 6 * scale
fig_w = 8 * scale
node_size = 450 * scale
arrow_size= 15 * scale
col_reached = '#f003fc'
col_frontier = '#03fcd3'
col_goal = '#88fc03'
col_initial = '#fc0362'
col_white = '#ffffff'
col_black = '#000000'


def pyplot_printer(it, problem, frontier, reached, curr, solution, folder=None, interactive=True):
    '''
    Use NetworkX + Matplotlib for displaying a snapshot of the search.

    '''

    if folder is None:
        folder = 'test'

    if it == 0:

        if not interactive:
            if os.path.isdir(folder):
                rmtree(folder)

            os.mkdir(folder)

    G = problem.to_graph()
    pos = nx.get_node_attributes(G, 'pos')

    
    if None in pos.values():
        # when unset positions are present, use force-directed layout
        pos = nx.spring_layout(G)

    initial_node = {problem.initial}
    goal_nodes = set(problem.goals)
    frontier_nodes = set(n.state for n in frontier)
    reached_nodes = set(reached) - frontier_nodes
    regular_nodes = set(G.nodes) - initial_node - goal_nodes

    if curr is not None:
        nx.draw_networkx_nodes(G, pos, nodelist=[curr.state], linewidths=2,
                               edgecolors=col_black,
                               node_color=col_white,
                               node_shape='s',
                               node_size=2*node_size)


    nx.draw_networkx_nodes(G, pos, nodelist=reached_nodes,
                           alpha=1, node_color=col_reached, edgecolors=col_black, node_size=1.8*node_size)
    nx.draw_networkx_nodes(G, pos, nodelist=frontier_nodes,
                           alpha=1, node_color=col_frontier, edgecolors=col_black, node_size=1.8*node_size)
    nx.draw_networkx_nodes(G, pos, nodelist=goal_nodes,
                           alpha=1, node_color=col_goal, edgecolors=col_black, node_size=1.0*node_size)
    nx.draw_networkx_nodes(G, pos, nodelist=initial_node,
                           alpha=1, node_color=col_initial, edgecolors=col_black, node_size=1.0*node_size)
    nx.draw_networkx_nodes(G, pos, nodelist=regular_nodes,
                           alpha=1, node_color=col_white, edgecolors=col_black, node_size=1.0*node_size)

        
    
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, arrowsize=arrow_size, connectionstyle=f'arc3, rad = 0.15')

    costs = {e : G.edges[e]['cost'] for e in G.edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=costs)

    if solution is not None and isinstance(solution, Solution):
        edgelist = []
        for i in range(len(solution)-1):
            edgelist.append((solution[i].state, solution[i+1].state))
        
        nx.draw_networkx_edges(G, pos, edgelist=edgelist, width=1.5, edge_color=col_goal,
                               arrowsize=arrow_size*1.5, connectionstyle=f'arc3, rad = 0.15')



    if problem.is_weighted(): # different costs
        cost_dict = {e : G.edges[e]['cost'] for e in G.edges}
        nx.draw_networkx_edge_labels(G, pos, cost_dict)


    if interactive:
        plt.show()
    else:
        plt.savefig(os.path.join(folder, f'{it}.png'), dpi=150, bbox_inches='tight', transparent=True)

    plt.clf()
