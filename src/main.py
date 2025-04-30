from maze_window import Window
from maze import Point, Line, Cell, Maze
from generators import generators
from solvers import solvers
from unittest.mock import patch
import time

def main():
    testing = True;
    while testing:
        win = Window(800, 600)

        start9 = time.time()
        maze = Maze(25, 25, 50, 50, generators["wilson"], win)
        maze.solve(solvers["bidir"])
        end9 = time.time()
        print(f"Wilson time:       {end9 - start9:.6f} seconds")
        time.sleep(2)
        win.clear()

        start7 = time.time()
        maze = Maze(25, 25, 50, 50, generators["wilson"], win)
        maze.solve(solvers["dead"])
        end7 = time.time()
        print(f"Wilson time:       {end7 - start7:.6f} seconds")
        time.sleep(2)
        win.clear()

        start8 = time.time()
        maze = Maze(25, 25, 50, 50, generators["wilson"], win)
        maze.solve(solvers["lefthand"])
        end8 = time.time()
        print(f"Wilson time:       {end8 - start8:.6f} seconds")
        time.sleep(2)
        win.clear()

        start5 = time.time()
        maze = Maze(25, 25, 50, 50, generators["wilson"], win)
        maze.solve(solvers["r_back"])
        end5 = time.time()
        print(f"DFS time:       {end5 - start5:.6f} seconds")
        time.sleep(2)
        win.clear()

        start = time.time()
        maze = Maze(25, 25, 50, 50, generators["wilson"], win)
        maze.solve(solvers["a_star"])
        end = time.time()
        print(f"Wilson time:     {end - start:.6f} seconds")
        time.sleep(2)
        win.clear()

        start2 = time.time()
        maze = Maze(25, 25, 50, 50, generators["prim"], win)
        maze.solve(solvers["dijk"])
        end2 = time.time()
        print(f"Prim time:     {end2 - start2:.6f} seconds")
        time.sleep(2)
        win.clear()

        start3 = time.time()
        maze = Maze(25, 25, 50, 50, generators["kruskal"], win)
        maze.solve(solvers["bfs"])
        end3 = time.time()
        print(f"Kruskal time:     {end3 - start3:.6f} seconds")
        time.sleep(2)
        win.clear()

        start4 = time.time()
        maze = Maze(25, 25, 50, 50, generators["dfs_r"], win)
        maze.solve(solvers["dfs"])
        end4 = time.time()
        print(f"DFS_R time:     {end4 - start4:.6f} seconds")
        time.sleep(2)
        win.clear()

        start5 = time.time()
        maze = Maze(25, 25, 50, 50, generators["dfs"], win)
        maze.solve(solvers["best_f"])
        end5 = time.time()
        print(f"DFS time:       {end5 - start5:.6f} seconds")
        time.sleep(2)
        win.clear()

        start6 = time.time()
        maze = Maze(25, 25, 50, 50, generators["dfs"], win)
        maze.solve(solvers["dfs_r"])
        end6 = time.time()
        print(f"DFS time:       {end6 - start6:.6f} seconds")
        time.sleep(2)


        testing = False
   
    win.wait_for_close()

main()    

    
