from maze_window import Window
from maze import Point, Line, Cell, Maze
from generators import generators
from unittest.mock import patch
import time

def main():
    while True:
        win = Window(800, 600)
        start = time.time()
        maze = Maze(25, 25, 50, 50, generators["wilson"], win)
        end = time.time()
        print(f"Wilson time:     {end - start:.6f} seconds")
        time.sleep(2)

        start2 = time.time()
        maze = Maze(25, 25, 50, 50, generators["prim"], win)
        end2 = time.time()
        print(f"Prim time:     {end2 - start2:.6f} seconds")
        time.sleep(2)

        start3 = time.time()
        maze = Maze(25, 25, 50, 50, generators["kruskal"], win)
        end3 = time.time()
        print(f"Kruskal time:     {end3 - start3:.6f} seconds")
        time.sleep(2)

        start4 = time.time()
        maze = Maze(25, 25, 50, 50, generators["dfs_r"], win)
        end4 = time.time()
        print(f"DFS_R time:     {end4 - start4:.6f} seconds")
        time.sleep(2)

        start5 = time.time()
        maze = Maze(25, 25, 50, 50, generators["dfs"], win)
        end5 = time.time()
        print(f"DFS time:       {end5 - start5:.6f} seconds")
        time.sleep(2)

        start6 = time.time()
        maze = Maze(25, 25, 50, 50, generators["wilsonAI"], win)
        end6 = time.time()
        print(f"Wilson GPT Dearest, time:     {end6 - start6:.6f} seconds")
        time.sleep(2)

        return False

    win.wait_for_close()

main()    

    
