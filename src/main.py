from maze_window import Window
from point import Point, Line, Cell, Maze

def main():
    win = Window(800, 600)
    maze = Maze(25, 25, 100, 100, win)
    win.wait_for_close()

main()    

    
