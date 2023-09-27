

import matplotlib.pyplot as plt
import networkx as nx
import os
from shutil import rmtree

from utils import Solution

def pyplot_printer(it, problem, frontier, reached, curr, solution, folder=None, pos=None, interactive=False):
    '''
    Use NetworkX + Matplotlib for displaying a snapshot of the search.

    '''
    node_size = 250
    arrow_size=15
    # '#264653'
    col_r = '#2a9d8f'
    col_f = '#e9c46a'
    col_g = '#f4a261'
    col_i = '#e76f51'
    col_w = '#ffffff'
    col_b = '#000000'

    if folder is None:
        folder = 'test'

    if it == 0:

        if not interactive:
            if os.path.isdir(folder):
                rmtree(folder)

            os.mkdir(folder)       

    G = problem.to_graph()

    if pos is None:
        pos = nx.spring_layout(G)

    initial_node = {problem.initial}
    goal_nodes = set(problem.goals)
    frontier_nodes = set(n.state for n in frontier)
    reached_nodes = set(reached) - frontier_nodes
    regular_nodes = set(G.nodes) - initial_node - goal_nodes

    if curr is not None:
        nx.draw_networkx_nodes(G, pos, nodelist=[curr.state], linewidths=2,
                               edgecolors=col_b,
                               node_color=col_w,
                               node_shape='s',
                               node_size=2*node_size)

    nx.draw_networkx_nodes(G, pos, nodelist=reached_nodes,
                           alpha=1, node_color=col_r, edgecolors=col_b, node_size=1.8*node_size)
    nx.draw_networkx_nodes(G, pos, nodelist=frontier_nodes,
                           alpha=1, node_color=col_f, edgecolors=col_b, node_size=1.8*node_size)
    nx.draw_networkx_nodes(G, pos, nodelist=goal_nodes,
                           alpha=1, node_color=col_g, edgecolors=col_b, node_size=1.0*node_size)
    nx.draw_networkx_nodes(G, pos, nodelist=initial_node,
                           alpha=1, node_color=col_i, edgecolors=col_b, node_size=1.0*node_size)
    nx.draw_networkx_nodes(G, pos, nodelist=regular_nodes,
                           alpha=1, node_color=col_w, edgecolors=col_b, node_size=1.0*node_size)

        
    
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, arrowsize=arrow_size, connectionstyle=f'arc3, rad = 0.25')

    if solution is not None and isinstance(solution, Solution):
        edgelist = []
        for i in range(len(solution)-1):
            edgelist.append((solution[i].state, solution[i+1].state))
        
        nx.draw_networkx_edges(G, pos, edgelist=edgelist, width=1.5, edge_color=col_g,
                               arrowsize=arrow_size*1.5, connectionstyle=f'arc3, rad = 0.25')


    if problem.is_weighted(): # different costs
        cost_dict = {e : G.edges[e]['cost'] for e in G.edges}
        nx.draw_networkx_edge_labels(G, pos, cost_dict)


    if interactive:
        plt.show()
    else:
        plt.savefig(os.path.join(folder, f'{it}.png'), dpi=150, bbox_inches='tight', transparent=True)

    plt.clf()    
