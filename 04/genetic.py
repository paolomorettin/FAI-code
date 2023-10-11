
from utils import select_choice

feats = [['H', 'S', 'F'],
         ['L', 'T', 'O'],
         ['M', 'Y', 'G']]


def pp(p):
    return f"[{feats[0][p[0]]}-{feats[1][p[1]]}-{feats[2][p[2]]}]"

def select_parents(pop, obj, choices):

    i1, _ = select_choice([(i, obj(p)) for i, p in enumerate(pop)],
                       choices)
    i2, _ = select_choice([(i, obj(p)) for i, p in enumerate(pop)
                        if i != i1],
                       choices)
    return pop[i1], pop[i2]
    


def reproduce(p1, p2, choices):
    split, _ = select_choice([(1,1), (2,1)], choices)
    return p1[0:split] + p2[split:]


def mutate(p, p_mutation, choices):
    mutated = []
    for i in range(3):
        mf, _ = select_choice([(p[i], 1 - p_mutation),
                               ((p[i]+1) % 3, p_mutation / 2),
                               ((p[i]+2) % 3, p_mutation / 2)],
                              choices)
        mutated.append(mf)

    return tuple(mutated)


def genetic(obj, pop, choices, max_it=10, p_mutation=0.1):

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
            p1, p2 = select_parents(pop, obj, choices)
            child = reproduce(p1, p2, choices)
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

    choices = [0.2, 0.9, 0.5, 0.1]
    p_mutation = 0.2
    max_it = 5

    initial = [(0,0,0),
               (0,1,0),
               (0,0,1),
               (1,0,1)]

    obj = lambda p : sum(p)

    print("Initial population")
    for p in initial:
        print(pp(p), 'fitness:', obj(p))

    genetic(obj, initial, choices,
            max_it=max_it, p_mutation=p_mutation)
                


        

        
        
