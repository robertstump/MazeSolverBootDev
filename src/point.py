

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

class Cell():
    def __init__(self, x1, y1, x2, y2, win):
        self.left_wall = True
        self.right_wall = True
        self.top_wall = True
        self.bottom_wall = True
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.win = win
        self.color = "red"

        self.left_top = Point(self.x1, self.y1)
        self.left_bot = Point(self.x1, self.y2)
        self.left_line = Line(self.left_top, self.left_bot)
        
        self.top_left = Point(self.x1, self.y1)
        self.top_right = Point(self.x2, self.y1)
        self.top_line = Line(self.top_left, self.top_right)

        self.right_top = Point(self.x2, self.y1)
        self.right_bot = Point(self.x2, self.y2)
        self.right_line = Line(self.right_top, self.right_bot)
    
        self.bot_left = Point(self.x1, self.y2)
        self.bot_right = Point(self.x2, self.y2)
        self.bottom_line = Line(self.bot_left, self.bot_right)

    def draw(self):
        if self.left_wall:
            self.left_line.draw(self.win.canvas, self.color)

        if self.top_wall:
            self.top_line.draw(self.win.canvas, self.color)

        if self.right_wall:
            self.right_line.draw(self.win.canvas, self.color)

        if self.bottom_wall:
            self.bottom_line.draw(self.win.canvas, self.color)
        
