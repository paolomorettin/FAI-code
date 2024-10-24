# FAI-code
Python3 code for the Fundamentals of AI course lab.

Feel free to reuse / distribute / contribute.

# Contributors:
Mattia Rigon (2023) - Added support for LRTA* with non-uniform action costs.
Alessandro Moscatelli (2024) - Added novel exercise types and quality-of-life changes.

## LABS 02/03 - Search algorithms

Extra required packages: `matplotlib`, `networkx`, `numpy`.

In `search/`, run: `python3 search.py alg`, where `alg` in `{bfs, dfs, ucs, greedy, astar}`


## LAB 04 - Non-conventional search

Extra required packages: `matplotlib`, `networkx`, `numpy`, `seaborn`.

All the examples are located in `nonconventional-search/`.

### Hill-climbing

To run hill-climbing on 2D grid problems, go to `hill_climbing` and
execute: `python3 hill_climbing.py alg`, where `alg` in `[steepest,
stochastic, stochastic-unweighted]`. Use the `-h` flag for help on
optional arguments.


### Genetic algorithms

To run the genetic seach algorithm on the Master Sandwitch problem,
try: `python3 genetic.py`. Use the `-h` flag for help on optional
arguments.


### Online search

To run the online seach algorithms on Maze problems,
try: `python3 online_search.py alg`, where `alg` in `[odfs,
lrtastar]`. Use the `-h` flag for help on
optional arguments.
