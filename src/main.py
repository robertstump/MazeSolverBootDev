from maze_window import Window
from maze import Point, Line, Cell, Maze
from generators import generators

def main():
    win = Window(800, 600)
    maze = Maze(25, 25, 100, 100, win)
    maze.generate(generators["dfs"])
    win.wait_for_close()

main()    

    
