from maze_window import Window
from point import Point, Line, Cell

def main():
    win = Window(800, 600)
    cell1 = Cell(20, 20, 40, 40, win)
    cell2 = Cell(40, 20, 60, 40, win)
    cell1.draw()
    cell2.draw()
    win.wait_for_close()

main()    

    
