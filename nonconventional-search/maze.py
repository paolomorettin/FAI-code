
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

       

class Maze:

    def __init__(self, side):

        self.G = nx.Graph()
        self.side = side
        for x in range(side+1):
            for y in range(side+1):
                self.G.add_node((x,y))

        self.init = None
        self.goal = None


    def random(self, seed, init=None, goal=None, max_cost=None):

        def neighbors(curr):
            x, y = curr
            neigh = []

            if y+1 <= self.side: neigh.append((x, y+1))
            if x+1 <= self.side: neigh.append((x+1, y))
            if y-1 >= 0: neigh.append((x, y-1))
            if x-1 >= 0: neigh.append((x-1, y))

            return neigh

        np.random.seed(seed)

        # generate edges
        reached = {(0,0)}# if init is None else init}
        while True:
            candidates = {(r, rn) for r in reached for rn in neighbors(r)
                          if rn not in reached}

            if len(candidates) == 0:
                break

            r, rn = list(candidates)[np.random.randint(len(candidates))]

            if max_cost is None:
                c = 1
            else:
                c = np.random.randint(1, max_cost + 1)
            
            self.G.add_edge(r, rn, cost=c)
            reached.add(rn)

        if init is not None:
            self.init = init
        else:
            candidates = list(self.G.nodes)
            self.init = candidates[np.random.randint(0, len(candidates))]

        if goal is not None:
            self.goal = goal
        else:
            candidates = list(set(self.G.nodes) - {self.init})
            self.goal = candidates[np.random.randint(0, len(candidates))]



    def actions(self, node):
        x, y = node
        adj = self.G[node]
        alist = []
        if (x, y+1) in adj: alist.append('N')
        if (x+1, y) in adj: alist.append('E')
        if (x, y-1) in adj: alist.append('S')
        if (x-1, y) in adj: alist.append('W')

        return alist

    def cost(self, node, action):
        x, y = node
        if action == 'N': nxt = (x, y+1)
        elif action == 'E': nxt = (x+1, y)
        elif action == 'S': nxt = (x, y-1)
        elif action == 'W': nxt = (x-1, y)

        assert((node, nxt) in self.G.edges)
        return self.G.edges[(node, nxt)]['cost']


    def execute(self, node, action):
        x, y = node
        if action == 'N': nxt = (x, y+1)
        elif action == 'E': nxt = (x+1, y)
        elif action == 'S': nxt = (x, y-1)
        elif action == 'W': nxt = (x-1, y)

        assert((node, nxt) in self.G.edges)
        return nxt
            
        


    def plot(self, curr=None, path=None):

        n_size = 1200
        n_shape = 's'
        e_size=15
        # '#264653'
        col_reached = '#f003fc'
        col_goal = '#88fc03'
        col_initial = '#fc0362'
        col_white = '#ffffff'
        col_black = '#000000'

        pos = {n : n for n in self.G.nodes}

        other_nodes = set(self.G.nodes) - {self.goal, self.init}

        if curr is not None:
            nx.draw_networkx_nodes(self.G, pos, nodelist=[curr],
                                   node_color=col_reached, edgecolors=col_black,
                                   node_size=1.5*n_size, node_shape=n_shape)

        nx.draw_networkx_nodes(self.G, pos, nodelist=[self.goal],
                               node_color=col_goal, edgecolors=col_black,
                               node_size=n_size, node_shape=n_shape)
            
        nx.draw_networkx_nodes(self.G, pos, nodelist=[self.init],
                               node_color=col_initial, edgecolors=col_black,
                               node_size=n_size, node_shape=n_shape)

        nx.draw_networkx_nodes(self.G, pos, nodelist=other_nodes,
                               node_color=col_white, edgecolors=col_black,
                               node_size=n_size, node_shape=n_shape)

        strlabels = {n : f'{n[0]},{n[1]}' for n in self.G.nodes}
        nx.draw_networkx_labels(self.G, pos, labels=strlabels)
        nx.draw_networkx_edges(self.G, pos, width=e_size)
        costs = nx.get_edge_attributes(self.G, 'cost')
        if len(set(costs.values())) > 1:
            nx.draw_networkx_edge_labels(self.G, pos, edge_labels=costs)

        plt.gca().set_aspect('equal')

        if path is None:
            plt.show()
        else:
            plt.savefig(path, dpi=150, bbox_inches='tight', transparent=True)

        plt.clf()


if __name__ == '__main__':

    side = 3
    m = Maze(side)
    m.random(666, init=(0,0), goal=(side, side), max_cost=4)
    m.plot()
    #m.plot(path='big_maze.png')
