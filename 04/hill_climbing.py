

from utils import all_neighbors, select_choice

hc_modes = ['steepest', 'stochastic (unweighted)', 'stochastic', 'first']




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
    
    higher_neighbors = [(n, obj(n)) for n in all_neighbors(curr, bounds=bounds)
                        if obj(n) > obj(curr)]

    if len(higher_neighbors) == 0: # best in neighborhood!
        return curr, it

    else:

        if mode == 'steepest':
            sorted_neighbors = sorted(higher_neighbors, key=lambda x : (x[1],x[0]))
            print("SORTED:", sorted_neighbors)
            nxt, _ = sorted_neighbors[-1]

        elif mode == 'stochastic':
            nxt, _ = select_choice(higher_neighbors, choices)

        elif mode == 'stochastic (unweighted)':
            unweighted_neighbors = [(n, 1) for n, _ in higher_neighbors]
            nxt, _ = select_choice(unweighted_neighbors, choices)

        elif mode == 'first':
            nxt = None
            for nxt, fn in higher_neighbors:
                what_to_do, _ = select_choice([('break', 0.5), ('continue', 0.5)], choices)
                if what_to_do  == 'break':
                    break

        else:
            raise NotImplementedError(f'Mode {mode} not in {hc_modes}')

        return hill_climbing(it+1, mode, obj, nxt, choices, bounds=bounds, printer=printer)


if __name__ == '__main__':

    import numpy as np
    from utils import generate_nonconvex, plt_printer

    xbounds = [0,10] # bounds to input variables
    ybounds = [0,20] # bounds to the objective function
    seed = 121 # generation seed
    initial = (5,4) # initial state

    np.random.seed(seed)

    # predetermined non-deterministic choices
    n_choices = 4
    choices = None #[round(np.random.random(), 1) for _ in range(n_choices)]
    

    # generating the objective function
    obj = generate_nonconvex(seed, xbounds=xbounds, ybounds=ybounds)

    hill_climbing(1, 'steepest', obj, initial, choices, bounds=xbounds, printer=plt_printer)

    '''
    for mode in hc_modes:
        hill_climbing(1, mode, obj, initial, choices, bounds=xbounds, printer=plt_printer)

    '''

                

