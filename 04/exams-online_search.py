
from sys import argv

from maze import Maze
from online_search import lrtastar, manhattan, online_dfs

def exam_printer(it, maze, s_curr, *args):

    print(s_curr)
    maze.plot(s_curr)


maze1 = Maze(2)
maze1.random(123, init=(1,1), goal=(0,0))

maze2 = Maze(2)
maze2.random(123, init=(0,0), goal=(2,2))

maze3 = Maze(2)
maze3.random(124, init=(0,0), goal=(2,1))

maze4 = Maze(2)
maze4.random(124, init=(2,0), goal=(0,2))


maze5 = Maze(2)
maze5.random(321, init=(1,1), goal=(0,0))

maze6 = Maze(2)
maze6.random(321, init=(2,0), goal=(2,2))

maze7 = Maze(2)
maze7.random(421, init=(0,0), goal=(2,1))

maze8 = Maze(2)
maze8.random(422, init=(2,0), goal=(0,2))



if len(argv) < 4:
    print("Usage: python3 exams-online_search.py YEAR N_EXAM N_VERSION")
    exit(1)

year, n_exam, n_version = map(int, argv[1:])

assert(year >= 2024)
assert(n_exam > 0 and n_exam < 6)
assert(n_version > 0 and n_version < 5)

    
if year == 2024:

    if n_exam == 1:
        if n_version == 1:
            print("2024-01-11 version 1") ; lrtastar(maze1, manhattan, printer=exam_printer)
        elif n_version == 2:
            print("2024-01-11 version 2") ; lrtastar(maze2, manhattan, printer=exam_printer) 
        elif n_version == 3:
            print("2024-01-11 version 3") ; lrtastar(maze3, manhattan, printer=exam_printer)
        elif n_version == 4:
            print("2024-01-11 version 4") ; lrtastar(maze4, manhattan, printer=exam_printer)

    elif n_exam == 2:
        if n_version == 1:
            print("2024-02-20 version 1") ; online_dfs(maze5, printer=exam_printer)
        elif n_version == 2:
            print("2024-02-20 version 2") ; online_dfs(maze6, printer=exam_printer) 
        elif n_version == 3:
            print("2024-02-20 version 3") ; online_dfs(maze7, printer=exam_printer)
        elif n_version == 4:
            print("2024-02-20 version 4") ; online_dfs(maze8, printer=exam_printer)
