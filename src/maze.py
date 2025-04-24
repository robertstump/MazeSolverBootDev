import time, random

class Point():
    def __init__(self, x, y):
        if x < 0 or y < 0:
            raise ValueError("Point values must be positive")
        if isinstance(x, float) or isinstance(y, float):
            raise ValueError("Point values must be of type int")
        self.x = x
        self.y = y

class Line():
    def __init__(self, pointA, pointB):
        if pointA.x == pointB.x and pointA.y == pointB.y:
            raise ValueError("Points must contain different values for line creation")

        self.a = pointA
        self.b = pointB

    def draw(self, canvas, color):
        canvas.create_line(
            self.a.x, self.a.y, self.b.x, self.b.y, fill=color, width=2
            )

class Cell():
    def __init__(self, x1, y1, x2, y2, win=None):
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
        self.up = None
        self.down = None
        self.right = None
        self.left = None
        self.x_index = None
        self.y_index = None
        self.visited = False
        
        if self.win is not None:
            self.bg_color = self.win.canvas.cget("bg")

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

    def visit_cell(self):
        self.visited = True

    def del_left(self):
        self.left_wall = False
    def del_right(self):
        self.right_wall = False
    def del_top(self):
        self.top_wall = False
    def del_bot(self):
        self.bottom_wall = False

    def draw(self):
        if self.left_wall:
            self.left_line.draw(self.win.canvas, self.color)
        else:
            self.left_line.draw(self.win.canvas, self.bg_color)

        if self.top_wall:
            self.top_line.draw(self.win.canvas, self.color)
        else:
            self.top_line.draw(self.win.canvas, self.bg_color)

        if self.right_wall:
            self.right_line.draw(self.win.canvas, self.color)
        else:
            self.right_line.draw(self.win.canvas, self.bg_color)

        if self.bottom_wall:
            self.bottom_line.draw(self.win.canvas, self.color)
        else:
            self.bottom_line.draw(self.win.canvas, self.bg_color)
    
    def draw_move(self, to_cell, undo=False):
        start = Point(int(self.x1 + (self.x2 - self.x1)/2), int(self.y1 - (self.y1 - self.y2)/2))
        end = Point(int(to_cell.x1 + (to_cell.x2 - to_cell.x1)/2), int(to_cell.y1 - (to_cell.y1 - to_cell.y2)/2))
        move_line = Line(start, end)
        if undo:
            move_line.draw(self.win.canvas, "gray")
        else:
            move_line.draw(self.win.canvas, self.color)

class Maze():
    def __init__(self, x1, y1, cell_size_x, cell_size_y, generator_function, win=None, rows=None, cols=None, seed=None):
        if cell_size_x < 1 or cell_size_y < 1:
            raise ValueError("Cell size in x and y  must be positive values")
        if isinstance(cell_size_y, float) or isinstance(cell_size_x, float):
            raise ValueError("Cell size must be passed as integer values")
        if win:
            if win.width < cell_size_x:
                raise ValueError("Window must be wider than cell width")
            if win.height < cell_size_y:
                raise ValueError("Window must be taller than cell height")

        self.x1 = x1
        self.y1 = y1
        self.size_x = cell_size_x
        self.size_y = cell_size_y
        self.win = win
        self.cells = []
        self.width = cols
        self.height = rows
        self.generator_function = generator_function
        
        if seed is not None:
            self.seed = seed
        else:
            self.seed = random.randint(0, 10000)
        self.rng = random.Random(self.seed)

        if self.width is not None and self.win is not None:
            if self.width * self.size_x > win.width:
                raise ValueError("Total maze width must fit in window width")
        if self.height is not None and self.win is not None:
            if self.height * self.size_y > win.height:
                raise ValueError("Total maze height must fit in window height")
        self._create_cells()

    def _create_cells(self):
        if self.win and hasattr(self.win, "canvas"):
            inner_width = self.win.width - self.x1 - self.x1
            inner_height = self.win.height - self.y1 - self.y1 
        if self.width is None: 
            self.width = int(inner_width / self.size_x)
        if self.height is None:
            self.height = int(inner_height / self.size_y)
        last_x = self.x1
        for i in range(self.width):
            column = []
            last_y = self.y1
            for j in range(self.height):
                tmp = Cell(last_x, last_y, last_x + self.size_x, last_y + self.size_y, self.win)
                column.append(tmp)
                last_y += self.size_y
            self.cells.append(column)     
            last_x += self.size_x
        
        for i in range(self.width):
            for j in range(self.height):
                self._index_neighbors(i, j)
                if self.win != None: 
                    self._draw_cells(i, j)

        if self.generator_function is not None:
            self.generate(self.generator_function)
            self._reset_visited()

    def _index_neighbors(self, x, y):
        assert len(self.cells[x]) > y, f"Column{x} has only {len(self.cells[x])}rows; tried y={y}"

        if x >= 1:
            left = self.cells[x - 1][y]
            self.cells[x][y].left = left
        if x < len(self.cells) - 1:
            right = self.cells[x + 1][y]
            self.cells[x][y].right = right
        if y >= 1:
            up = self.cells[x][y - 1]
            self.cells[x][y].up = up
        if y < len(self.cells[x]) - 1:
            down = self.cells[x][y + 1]
            self.cells[x][y].down = down

        self.cells[x][y].x_index = x
        self.cells[x][y].y_index = y


    def _draw_cells(self, i, j):
        self.cells[i][j].draw()
        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.005)

    def generate(self, generator_function):
        generator_function(self)

    def _reset_visited(self):
        for col in self.cells:
            for cell in col:
                cell.visited = False
