
import random
from utils import select_choice

hc_modes = ['steepest', 'stochastic-unweighted', 'stochastic']

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
    # Parametric univariate normal. Given mean and stdev, returns the
    # PDF f(x) s.t. x ~ N(mu, sigma).
    p_norm = lambda mu, sigma : (lambda x : np.exp((((x-mu)/sigma)**2)/-2)/(sigma*np.sqrt(2*np.pi)))

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





def hill_climbing(it, mode, obj, curr, choices, bounds=[0,10], printer=None):
    '''
    Recursive hill-climbing algorithm.

    mode -- one of 'hc_modes'
    obj -- objective function to be maximized
    curr -- current state
    choices -- predetermined list of choices (simulating stochasticity)
    bounds -- coordinate bounds of the state space

    '''

    print()
    print(f'Hill-climbing-{mode}, iteration: {it}, x: {curr}, f(x): {obj(curr)}')
    if printer is not None:
        printer(it, obj, bounds, curr)

    # neighboring solutions with *STRICTLY* higher objective
    higher_neighbors = [(n, obj(n)) for n in all_neighbors(curr, bounds=bounds)
                        if obj(n) > obj(curr)]

    if len(higher_neighbors) == 0: # best in neighborhood!
        return curr, it

    else:

        if mode == 'steepest':
            # sorted by obj first and state in case of tie
            sorted_neighbors = sorted(higher_neighbors, key=lambda x : (x[1],x[0]))
            nxt, _ = sorted_neighbors[-1]

        elif mode == 'stochastic':
            nxt, _ = select_choice(higher_neighbors, choices)

        elif mode == 'stochastic-unweighted':
            unweighted_neighbors = [(n, 1) for n, _ in higher_neighbors]
            nxt, _ = select_choice(unweighted_neighbors, choices)

        else:
            raise NotImplementedError(f'Mode {mode} not in {hc_modes}')

        return hill_climbing(it+1, mode, obj, nxt, choices, bounds=bounds, printer=printer)


if __name__ == '__main__':

    import numpy as np
    from utils import plt_printer
    import argparse
    
    # fixed problem parameters
    XBOUNDS = [0,10] # bounds to input variables
    YBOUNDS = [0,20] # bounds to the objective function
    
    parser = argparse.ArgumentParser()

    parser.add_argument('mode', type=str,
                        help=f"HC mode in {hc_modes}")


    parser.add_argument('--initial', type=int, nargs=2,
                        help=f"initial coordinates",
                        default=(5,4))

    parser.add_argument('--choices', type=float, nargs='+',
                        help=f"predetermined non-deterministic choices",
                        default=None)
    
    parser.add_argument('--seed', type=int,
                        help="Random seed number",
                        default=int(random.random() * 1000))

    args = parser.parse_args()

    np.random.seed(args.seed)
    if args.choices == None:
        args.choices = [round(np.random.uniform(0, 1), 2) for x in range(0, 3)]
    
    print(f"CHOICES: {args.choices}\nSEED: {args.seed}")

    # generating the objective function
    obj = generate_nonconvex(args.seed, xbounds=XBOUNDS, ybounds=YBOUNDS)


    if args.mode not in hc_modes:
        raise NotImplementedError(f"HC mode '{args.mode}' not implemented.")

    hill_climbing(1, args.mode, obj, args.initial, args.choices,
                  bounds=XBOUNDS, printer=plt_printer)
