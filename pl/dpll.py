import numpy as np
import networkx as nx
from utils import unsatisfied_clauses

def find_unit_clause(symbols, clauses, model):
    save_index = None
    for clause in clauses:
        i = 0
        sat = False
        c_none = 0
        while i < len(clause):
            literal_index = symbols.index(clause[i].replace('!', ''))
            if model[literal_index] == None: 
                save_index = i
                c_none = c_none + 1
            elif model[literal_index] == True: 
                sat = True
            i = i + 1
        if c_none == 1 and not sat:
                return clause[save_index]
    return None

def find_first(model):
    i = 0
    while i < len(model):
        if model[i] == None:
            return i
        i = i + 1
    return None

def dpll_satisfailable(clauses):
    symbols = set([x.replace('!', '') for x in list(itertools.chain.from_iterable(cnf))])
    symbols = sorted(list(symbols), key=lambda x: re.sub('[^A-Za-z]+', '', x).lower())

    model = [None] * len(symbols)

    search_tree = nx.Graph()
    search_tree.add_node(0)
    
    labels = {0:'Start'}
    return (dpll(clauses, symbols, model, search_tree, 0, labels), search_tree, labels)

def dpll(clauses, symbols, model, search_tree, parent_node, labels):
    unsat_clauses = unsatisfied_clauses(symbols, clauses, model)
    print(model)
    if unsat_clauses != None:
        if len(unsat_clauses) == 0:
            id = search_tree.number_of_nodes()
            search_tree.add_node(id)
            search_tree.add_edge(parent_node, id)
            labels[id] = 'SAT'
            return True
        else:
            # I have at least one clause unsatisfailable with the current model
            id = search_tree.number_of_nodes()
            search_tree.add_node(id)
            search_tree.add_edge(parent_node, id)
            labels[id] = 'FAIL'
            return False
    else:
        lonely_literal = find_unit_clause(symbols, clauses, model)
        if lonely_literal != None:
            literal = lonely_literal
            new_model = [x for x in model]
            if ('!' in literal):
                new_model[symbols.index(literal.replace('!', ''))] = False 
            else: 
                new_model[symbols.index(literal.replace('!', ''))] = True

            id = search_tree.number_of_nodes()
            search_tree.add_node(id)
            search_tree.add_edge(parent_node, id)
            labels[id] = literal

            return dpll(clauses, symbols, new_model, search_tree, id, labels)
        else:
            # QUESTION: is the first symbol of the list or the first found on the clauses?
            literal_index = find_first(model)
            ans = None
            # Model setting the literal to true
            new_model_true = [x for x in model]
            new_model_true[literal_index] = True
            
            id = search_tree.number_of_nodes()
            search_tree.add_node(id)
            search_tree.add_edge(parent_node, id)
            labels[id] = symbols[literal_index]

            ans = dpll(clauses, symbols, new_model_true, search_tree, id, labels)

            # Model setting the literal to false
            new_model_false = [x for x in model]
            new_model_false[literal_index] = False

            id = search_tree.number_of_nodes()
            search_tree.add_node(id)
            search_tree.add_edge(parent_node, id)
            labels[id] = '!' + symbols[literal_index]

            ans = ans or dpll(clauses, symbols, new_model_false, search_tree, id, labels)

            return ans



if __name__ == '__main__':
    import argparse
    import itertools
    import re
    import matplotlib.pyplot as plt
    from networkx.drawing.nx_pydot import graphviz_layout
    from utils import generate_cnf, hierarchy_pos

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--conjunctions', type=int,
                    help=f"Number of conjunctions in the formula",
                    default=4)
    parser.add_argument('-d', '--disjunctions', type=int, nargs=2,
                    help=f"Limit of minimum and maximum disjunctions in the formula",
                    default=(1, 4))
    
    parser.add_argument('-l', '--literals', type=str, nargs="+",
                    help=f"Literal list from which the formula is created",
                    default=['A', 'B', 'C', 'D', 'E', 'F'])

    parser.add_argument('-s', '--seed', type=int,
                    help=f"Random seed number",
                    default=int(np.random.random() * 1000))

    args = parser.parse_args()

    np.random.seed(args.seed)
    print("SEED: ", args.seed)
    symbols = args.literals

    if len(symbols) < args.disjunctions[1]:
        raise AssertionError("Number of literals " +
                             "is not sufficient to generate a formula " +
                             "with maximum disjunctions")

    cnf = generate_cnf(symbols, args.conjunctions, args.disjunctions[1], min_disj=args.disjunctions[0])
    print(cnf)

    input()
    (ans, search_tree, labels) = dpll_satisfailable(cnf)

    print(f"Solution of symbols {symbols} is {ans}")

    nx.draw(search_tree, pos=hierarchy_pos(search_tree, 0), labels=labels)
    plt.show()