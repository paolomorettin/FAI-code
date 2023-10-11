
import matplotlib.patches as patches
import matplotlib.pyplot as plt

import seaborn as sns

import numpy as np


''' Parametric univariate normal. Given mean and stdev, returns the
PDF f(x) s.t. x ~ N(mu, sigma).

'''
p_norm = lambda mu, sigma : (lambda x : np.exp((((x-mu)/sigma)**2)/-2)/(sigma*np.sqrt(2*np.pi)))


def select_choice(options, choices):
    '''Simulated stochastic process that deterministically pick an
    option given a pre-determined list of choices. Choices are
    cycled through. Options are weighted.

    '''
    choice = choices.pop(0) 
    choices.append(choice) # cycling

    w_sum = sum(w for _, w in options)
    p = 0
    for opt, w in options:
        p += w/w_sum
        if choice <= p:
            return opt, p


def all_neighbors(current_state, bounds=[0,10]):
    '''
    Returns the list all 8-neighbors in a 2D grid, in this order:

    SW, S, SE, W, -, E, NW, N, NE

    '''

    xc, yc = current_state
    return [(xn, yn)
            for yn in [yc-1, yc, yc+1]                  # the 9-tiles square centered in (xc, yc)
            for  xn in [xc-1, xc, xc+1]
            if ((xn != xc) or (yn != yc))               # minus (xc, yc) itself
            and xn >= bounds[0] and xn < bounds[1]
            and yn >= bounds[0] and yn < bounds[1]]     # and the states out of bounds


def generate_nonconvex(seed, xbounds=[0,10], ybounds=[0,99], n_modes=7):
    '''Generates a non-convex function by sampling a mixture of
    'n_modes' 2d-gaussians.

    '''
    np.random.seed(seed)
    rng = np.random.random
    xmin, xmax = xbounds

    params = []                             
    for _ in range(n_modes):
        mode = (rng() * xmax, rng() * xmax)
        stdev = xmax/n_modes #rng() * (xmax - xmin)
        weight = 1
        params.append((mode, stdev, weight))

    opt = lambda xy : sum(p3 \
                          * p_norm(p1[0],p2)(xy[0]) \
                          * p_norm(p1[1],p2)(xy[1])
                          for p1, p2, p3 in params)

    max_opt = max(opt((x,y)) for x in range(xmin, xmax)
                  for y in range(xmin, xmax))

    ymin, ymax = ybounds
    norm_opt = lambda xy : ymin + int(opt(xy)*(ymax-ymin)/max_opt)

    return norm_opt


def plt_printer(it, opt, bounds, curr, path=None):

    col_curr = '#00ff00'

    bmin, bmax = bounds
    xopt = np.array([[opt((x, y)) for x in range(bmin, bmax)]
                     for y in range(bmin, bmax)])
    
    ax = sns.heatmap(xopt, annot=True, cbar=False)


    if curr is not None:
        rect = patches.Rectangle(curr, 1, 1, linewidth=3, edgecolor=col_curr, facecolor='none')
        ax.add_patch(rect)

    ax.invert_yaxis()

    if path is not None:
        strpath = path(it)
        plt.savefig(strpath, dpi=150, bbox_inches='tight', transparent=True)
    else:
        plt.show()

    plt.clf()



if __name__ == '__main__':

    options = [(i, 1) for i in range(4)]
    choices = [0.2, 0.6, 0.3]

    print(select_choice(options, choices))
    print(select_choice(options, choices))
    print(select_choice(options, choices))
    print(select_choice(options, choices))


    

    

    

    
                          

    
