import numpy as np
from utils import select_choice, unsatisfied_clauses

def maximize_satisfied(symbols, clauses, model, target_clause):
    best_literal = None
    min_unsat = len(clauses) # Maximize sat should be equal to minimizing unsat

    for literal in target_clause:
        new_model = [x for x in model]
        new_model[symbols.index(literal.replace('!', ''))] = not model[symbols.index(literal.replace('!', ''))]
        curr_sat = len(unsatisfied_clauses(symbols, clauses, new_model))
        print(f"Literal {literal.replace('!', '')} leaves the model with {curr_sat} unsitisfied clauses")
        if(curr_sat < min_unsat):
            min_unsat = curr_sat
            best_literal = literal.replace('!', '')

    return best_literal

def walksat(symbols, clauses, choices, max_flips=1000, p = 0.5):
    model = np.zeros(len(symbols), dtype=bool)
    for i in range(len(model)):
        if np.random.random() < 0.5:
            model[i] = True
        else:
            model[i] = False

    print("Starting model: ", model)
    for _ in range(max_flips):
        input()
        unsat_clauses = unsatisfied_clauses(symbols, clauses, model)
        if len(unsat_clauses) == 0:
            return model
        (clause, _) = select_choice([(x, 1) for x in unsat_clauses], choices)
        print(f"Selected clause: {clause}")
        if select_choice([('Informed', 1 - p), ('Uninformed', p)], choices)[0] == 'Informed':
            print('Selected informed flip')
            to_flip = maximize_satisfied(symbols, clauses, model, clause)
            model[symbols.index(to_flip)] = not model[symbols.index(to_flip)]
            pass
        else:
            print('Selected random flip')
            options = [(x.replace('!', ''), 1) for x in clause]
            (to_flip, _) = select_choice(options, choices)
            model[symbols.index(to_flip)] = not model[symbols.index(to_flip)]
        print(f"Flipped {to_flip} that becomes {model[symbols.index(to_flip)]}")
    return None

if __name__ == '__main__':
    import argparse
    from utils import parse_formula, generate_cnf, get_symbols

    parser = argparse.ArgumentParser()

    parser.add_argument('--solve', type=str, nargs='+', 
                        help=f"List of literals in atrix form, where length of each clause is expressed in clause_lengths",
                        default=None)
    parser.add_argument('--clause_lengths', type=int, nargs='+',
                        help=f"A list that expresses the lenght of each clauses in solve",
                        default=None)

    parser.add_argument('-c', '--conjunctions', type=int,
                    help=f"Number of conjunctions in the formula",
                    default=4)
    parser.add_argument('-d', '--disjunctions', type=int, nargs=2,
                    help=f"Limit of minimum and maximum disjunctions in the formula",
                    default=(3, 4))
    
    parser.add_argument('-p', '--uninformed_probability', type=float,
                        help=f"Sets the probability of uninformed_search",
                        default=0.5)
    
    parser.add_argument('-l', '--literals', type=str, nargs="+",
                    help=f"Literal list from which the formula is created",
                    default=['A', 'B', 'C', 'D', 'E', 'F'])

    parser.add_argument('-s', '--seed', type=int,
                    help=f"Random seed number",
                    default=int(np.random.random() * 1000))
    parser.add_argument('--choices', type=float, nargs='+',
                        help=f"Predetermined non-deterministic choices",
                        default=None)

    args = parser.parse_args()

    np.random.seed(args.seed)
    temp_choices = [round(np.random.uniform(0, 1), 2) for x in range(0, 3)]
    if args.choices == None:
        args.choices = temp_choices

    print("SEED: ", args.seed)
    symbols = args.literals

    if len(symbols) < args.disjunctions[1]:
        raise ValueError("Number of literals " +
                             "is not sufficient to generate a formula " +
                             "with maximum disjunctions")

    if args.solve == None:
        cnf = generate_cnf(symbols, args.conjunctions, args.disjunctions[1], min_disj=args.disjunctions[0])
    elif args.solve != None and args.clause_lengths != None:
        cnf = parse_formula(args.solve, args.clause_lengths)
    else:
        raise ValueError('Formula or disjunctions lengths not provided')
    print(cnf)

    symbols = get_symbols(cnf)
    ans = walksat(symbols, cnf, args.choices, p = args.uninformed_probability)

    print(f"Formula: {cnf}")
    print(f"Solution of symbols {symbols} is {ans}")