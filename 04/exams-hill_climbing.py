
import numpy as np
from utils import generate_nonconvex, plt_printer
from hill_climbing import hill_climbing



xbounds = [0,16] # bounds to input variables
ybounds = [0,20] # bounds to the objective function
n_choices = 4
n_modes = 5

seed1 = 6 # generation seed
initial1 = (5,4) # initial state
np.random.seed(seed1)
choices1 = None #[round(np.random.random(), 1) for _ in range(n_choices)]
obj1 = generate_nonconvex(seed1, xbounds=xbounds, ybounds=ybounds, n_modes=n_modes)

seed2 = 6 # generation seed
initial2 = (14,12) # initial state
np.random.seed(seed2)
choices2 = None #[round(np.random.random(), 1) for _ in range(n_choices)]
obj2 = generate_nonconvex(seed2, xbounds=xbounds, ybounds=ybounds, n_modes=n_modes)

seed3 = 7 # generation seed
initial3 = (5,4) # initial state
np.random.seed(seed3)
choices3 = None #[round(np.random.random(), 1) for _ in range(n_choices)]
obj3 = generate_nonconvex(seed3, xbounds=xbounds, ybounds=ybounds, n_modes=n_modes)

seed4 = 14 # generation seed
initial4 = (2,8) # initial state
np.random.seed(seed4)
choices4 = None #[round(np.random.random(), 1) for _ in range(n_choices)]
obj4 = generate_nonconvex(seed4, xbounds=xbounds, ybounds=ybounds, n_modes=n_modes)

print("V1")
hill_climbing(1, 'steepest', obj1, initial1, choices1, bounds=xbounds, printer=plt_printer)


print("V2")
hill_climbing(1, 'steepest', obj2, initial2, choices2, bounds=xbounds, printer=plt_printer)

print("V3")
hill_climbing(1, 'steepest', obj3, initial3, choices3, bounds=xbounds, printer=plt_printer)

print("V4")
hill_climbing(1, 'steepest', obj4, initial4, choices4, bounds=xbounds, printer=plt_printer)













                

