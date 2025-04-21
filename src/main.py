from maze_window import Window
from point import Point, Line

def main():
    win = Window(800, 600)
    pointA = Point(200, 200)
    pointB = Point(600, 250)
    line = Line(pointA, pointB)
    line.draw(win.canvas, "red")
    
    win.wait_for_close()

main()    

    
