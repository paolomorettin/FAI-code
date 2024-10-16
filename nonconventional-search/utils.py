
import matplotlib.patches as patches
import matplotlib.pyplot as plt

import seaborn as sns

import numpy as np

def select_choice(options, choices):
    '''Simulated stochastic process that deterministically pick an
    option given a pre-determined list of choices. Choices are
    cycled through. Options are weighted.

    '''
    w_sum = sum(w for _, w in options)

    print("\t\toptions:", [(o, w/w_sum) for o,w in options])
    print("\t\tchoices:", choices)

    choice = choices.pop(0) 
    choices.append(choice) # cycling

    p = 0
    for opt, w in options:
        p += w/w_sum
        if choice <= p:
            return opt, p


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


    

    

    

    
                          

    
