
from utils import select_choice

FEATS = [['H', 'S', 'F', 'K'], # ham, salami, felafel, kebab
         ['L', 'T', 'O', 'B'], # lettuce, tomato, onion, bell peppers
         ['M', 'Y', 'G'], # mayonnaise, yogurt, garlic sauce
         ['B', 'W', 'P']] # bun, wrap, pita


def pp(p):
    #return f"[{FEATS[0][p[0]]}-{FEATS[1][p[1]]}-{FEATS[2][p[2]]}]"
    return "[" + "-".join([f"{FEATS[i][p[i]]}" for i in range(len(p))]) + "]"

def select_parents(pop, obj, choices):

    print("\tSelecting parents")
    
    i1 = int(select_choice([(f"individual {i}", obj(p)) for i, p in enumerate(pop)],
                           choices)[0].split(" ")[-1])

    print("\tparent1:", pp(pop[i1]))
    
    i2 = int(select_choice([(f"individual {i}", obj(p)) for i, p in enumerate(pop) if i != i1],
                           choices)[0].split(" ")[-1])

    print("\tparent2:", pp(pop[i2]))

    return pop[i1], pop[i2]
    


def reproduce(p1, p2, choices):
    
    assert(len(FEATS) == len(p1))
    assert(len(FEATS) == len(p2))
    split_points = list(range(len(FEATS)))[1:]

    print("\tCrossing:")
    split = int(select_choice([(f"split index {sp}",1) for sp in split_points],
                              choices)[0].split(" ")[-1])

    res = p1[0:split] + p2[split:]
    print("\tSplit point:", split, "result:", pp(res))
    return res


def mutate(p, p_mutation, choices):
    mutated = []
    for i in range(len(FEATS)):
        print(f"\tMutating bit {i}")
        # add 1 bit with probability p_mutation to the value at index i
        mf = int(select_choice([(f"keep value {p[i]}", 1 - p_mutation),
                                (f"mutate to {(p[i]+1) % len(FEATS[i])}", p_mutation)],
                               choices)[0].split(" ")[-1])
        mutated.append(mf)
        if mf == p[i]:
            print("\tno mutation")
        else:
            print("\t", p[i], "->", mf)

    return tuple(mutated)


def genetic(obj, pop, choices, max_it=10, p_mutation=0.1, interactive=False):

    it = 0
    best = sorted(pop, key=lambda x : obj(x))[-1]
    while it < max_it:
        next_pop = []
        curr_best = None
        
        print()
        print("ITERATION:", it)
        print("Best:", pp(best), 'fitness:', obj(best))
        print("Population:")
        for p in pop: print(pp(p), 'fitness:', obj(p))
        print()
        
        for i in range(len(pop)):

            if interactive: input()
            p1, p2 = select_parents(pop, obj, choices)

            if interactive: input()
            child = reproduce(p1, p2, choices)

            if interactive: input()
            mutated_child = mutate(child, p_mutation, choices)
            print("\t parent 1:", pp(p1), "parent 2:", pp(p2),
                  "made:", pp(child), "mutated:", pp(mutated_child))
            child = mutated_child

            next_pop.append(child)
            if curr_best is None or obj(curr_best) < obj(child):
                curr_best = child

        pop = next_pop
        if obj(curr_best) > obj(best):
            best = curr_best

        it += 1
        print()

    print("\n\nBEST:", pp(best), "fitness:", obj(best))
    return best


if __name__ == '__main__':

    import argparse
    from itertools import product
    import numpy as np

    # maximum iterations
    MAX_ITERS = 5
    
    parser = argparse.ArgumentParser()

    parser.add_argument('--pop-size', type=int,
                        help="(Constant) population size",
                        default=3)

    parser.add_argument('--p-mutation', type=float,
                        help=f"Probability of mutating one variable",
                        default=0.1)

    parser.add_argument('--choices', type=float, nargs='+',
                        help=f"predetermined non-deterministic choices",
                        default=[0.3, 0.99, 0.49, 0.01])
    
    parser.add_argument('--seed', type=int,
                        help="Random seed number",
                        default=666)

    args = parser.parse_args()
    print(f"CHOICES: {args.choices}\nSEED: {args.seed}\nPR.MUTATION: {args.p_mutation}")

    np.random.seed(args.seed)

    p_mutation = 0.2

    all_combinations = list(product(*[list(range(len(feats_i))) for feats_i in FEATS]))

    initial_population = [all_combinations[i]
                          for i in np.random.choice(range(len(all_combinations)),
                                                    args.pop_size,
                                                    replace=False)]

    # objective function
    obj = lambda p : sum(p) + 1

    genetic(obj, initial_population, args.choices,
            max_it=MAX_ITERS, p_mutation=args.p_mutation, interactive=True)
                


        

        
        
