

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, pointA, pointB):
        self.a = pointA
        self.b = pointB

    def draw(self, canvas, color):
        canvas.create_line(
            self.a.x, self.a.y, self.b.x, self.b.y, fill=color, width=2
            )
