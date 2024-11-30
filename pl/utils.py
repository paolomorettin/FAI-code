import numpy as np 

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
        
if __name__ == '__main__':

    options = [(i, 1) for i in range(4)]
    choices = [0.2, 0.6, 0.3]

    print(select_choice(options, choices))
    print(select_choice(options, choices))
    print(select_choice(options, choices))
    print(select_choice(options, choices))