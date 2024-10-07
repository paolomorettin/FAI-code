
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


    def random(self, seed, init=None, goal=None):

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
            self.G.add_edge(r, rn)
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
        col_r = '#2a9d8f'
        col_f = '#e9c46a'
        col_g = '#f4a261'
        col_i = '#e76f51'
        col_w = '#ffffff'
        col_b = '#000000'


        pos = {n : n for n in self.G.nodes}

        other_nodes = set(self.G.nodes) - {self.goal, self.init}

        if curr is not None:
            nx.draw_networkx_nodes(self.G, pos, nodelist=[curr],
                                   node_color=col_r, edgecolors=col_b,
                                   node_size=1.5*n_size, node_shape=n_shape)

        nx.draw_networkx_nodes(self.G, pos, nodelist=[self.goal],
                               node_color=col_g, edgecolors=col_b,
                               node_size=n_size, node_shape=n_shape)
            
        nx.draw_networkx_nodes(self.G, pos, nodelist=[self.init],
                               node_color=col_i, edgecolors=col_b,
                               node_size=n_size, node_shape=n_shape)

        nx.draw_networkx_nodes(self.G, pos, nodelist=other_nodes,
                               node_color=col_w, edgecolors=col_b,
                               node_size=n_size, node_shape=n_shape)

        strlabels = {n : f'{n[0]},{n[1]}' for n in self.G.nodes}
        nx.draw_networkx_labels(self.G, pos, labels=strlabels)
        nx.draw_networkx_edges(self.G, pos, width=e_size)

        plt.gca().set_aspect('equal')

        if path is None:
            plt.show()
        else:
            plt.savefig(path, dpi=150, bbox_inches='tight', transparent=True)

        plt.clf()


if __name__ == '__main__':

    side = 5
    m = Maze(side)
    m.random(666, init=(0,0), goal=(side, side))
    m.plot()
    #m.plot(path='big_maze.png')


            
                       
            
        



        

        
