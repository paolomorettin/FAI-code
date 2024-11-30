import numpy as np 
import re

def select_choice(options, choices):
    '''Simulated stochastic process that deterministically pick an
    option given a pre-determined list of choices. Choices are
    cycled through. Options are weighted.

    '''
    w_sum = sum(w for _, w in options)

    print("options:", [(o, w/w_sum) for o,w in options])
    print("choices:", choices)

    choice = choices.pop(0) 
    choices.append(choice) # cycling

    p = 0
    for opt, w in options:
        p += w/w_sum
        if choice <= p:
            return opt, p
        
def generate_cnf(symbols, n_conj, max_disj, min_disj = 1):
    '''
    Creates a random formula in cnd form. 
    The formula is expressed in a matrix where:
    each cell in each row is in the same disjuction and
    each row is in conjuction with the others
    '''

    cnf = []
    for conj in range(0, n_conj):
        choices = np.random.choice(
            len(symbols), 
            size=np.random.randint(min_disj, max_disj + 1), 
            replace=False)
        literals = []
        for x in range(len(choices)):
            if np.random.random() <= 0.5:
                literals.append('!' + symbols[choices[x]])
            else:
                literals.append('' + symbols[choices[x]])
        cnf.append(sorted(literals, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower()))
    return cnf

def unsatisfied_clauses(symbols, clauses, model):
    unsat = []
    for clause in clauses:
        sat = False
        for literal in clause:
            if('!' not in literal):
                sat = sat or model[symbols.index(literal)]
            else:
                sat = sat or not model[symbols.index(literal.replace('!', ''))]
        if not sat:
            unsat.append(clause)
    return unsat