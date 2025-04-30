import unittest
#from parameterized import parameterized
from unittest.mock import MagicMock, patch
from generators import generators
from solvers import solvers
from maze import Maze, Point, Line, Cell

class SetupTests(unittest.TestCase):
    #MAZE CREATION OVERALL WORKING
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, 10, 10, None, None, num_rows, num_cols) 
        self.assertEqual(len(m1.cells), num_cols)
        self.assertEqual(len(m1.cells[0]), num_rows)
    #POINT CREATION AND INPUT VALUES
    def test_create_point(self):
        point = Point(10, 10)
        self.assertEqual(point.x, 10)

    def test_negative_point(self):
        with self.assertRaises(ValueError):
            point = Point(-10, 10)
    
    def test_floating_point(self):
        with self.assertRaises(ValueError):
            point = Point(10.0, 10.5)
    #LINE CREATION AND INPUT VALUES
    def test_line_creation(self):
        pointA = Point(10, 10)
        pointB = Point(20, 10)
        line = Line(pointA, pointB)
        self.assertEqual(line.a, pointA)
        self.assertEqual(line.b, pointB)

    def test_line_draw(self):
        pointA = Point(10, 10)
        pointB = Point(10, 10)
        with self.assertRaises(ValueError):
            line = Line(pointA, pointB)
    #LINE METHOD TESTING
    def test_line_draw_call(self):
        pointA = Point(10, 10)
        pointB = Point(20, 10)
        line = Line(pointA, pointB)
        mock_canvas = MagicMock() 
        line.draw(mock_canvas, "red")

        mock_canvas.create_line.assert_called_once_with(10, 10, 20, 10, fill="red", width=2)
    #CELL CREATION AND INPUT
    def test_cell_create(self):
       cell = Cell(10, 10, 20, 20)
       self.assertEqual(cell.left_wall, True)
       self.assertEqual(cell.right_wall, True)
       self.assertEqual(cell.top_wall, True)
       self.assertEqual(cell.bottom_wall, True)
       self.assertEqual(cell.x1, 10)
       self.assertEqual(cell.y1, 10)
       self.assertEqual(cell.x2, 20)
       self.assertEqual(cell.y2, 20)
       self.assertEqual(cell.win, None)
       self.assertEqual(cell.color, "red")
    
    def test_cell_mock_win(self):
        mock_win = MagicMock()
        cell = Cell(10, 10, 20, 20, mock_win)
        self.assertEqual(cell.win, mock_win)
    #CELL DRAWING CALLS 
    def test_cell_draw_wall(self):
        mock_canvas = MagicMock()
        mock_win = MagicMock()
        mock_win.canvas = mock_canvas
        cell = Cell(10, 10, 20, 20, mock_win)
        cell.left_line.draw = MagicMock()
        cell.right_line.draw = MagicMock()
        cell.top_line.draw = MagicMock()
        cell.bottom_line.draw = MagicMock()

        cell.draw()

        cell.left_line.draw.assert_called_once()
        cell.right_line.draw.assert_called_once()
        cell.top_line.draw.assert_called_once()
        cell.bottom_line.draw.assert_called_once()

    def test_delete_left(self):
        mock_canvas = MagicMock()
        mock_win = MagicMock()
        mock_win.canvas = mock_canvas
        cell = Cell(10, 10, 20, 20, mock_win)
        cell.left_line.draw = MagicMock()
        cell.right_line.draw = MagicMock()
        cell.top_line.draw = MagicMock()
        cell.bottom_line.draw = MagicMock()
        
        cell.del_left()
        cell.draw()

        
        cell.left_line.draw.assert_called_once_with(cell.win.canvas, cell.bg_color)
        cell.right_line.draw.assert_called_once()
        cell.top_line.draw.assert_called_once()
        cell.bottom_line.draw.assert_called_once()
        
    def test_delete_right(self):
        mock_canvas = MagicMock()
        mock_win = MagicMock()
        mock_win.canvas = mock_canvas
        cell = Cell(10, 10, 20, 20, mock_win)
        cell.left_line.draw = MagicMock()
        cell.right_line.draw = MagicMock()
        cell.top_line.draw = MagicMock()
        cell.bottom_line.draw = MagicMock()

        cell.del_right()
        cell.draw()

        cell.left_line.draw.assert_called_once()
        cell.right_line.draw.assert_called_once_with(cell.win.canvas, cell.bg_color)
        cell.top_line.draw.assert_called_once()
        cell.bottom_line.draw.assert_called_once()

    def test_delete_top(self):
        mock_canvas = MagicMock()
        mock_win = MagicMock()
        mock_win.canvas = mock_canvas
        cell = Cell(10, 10, 20, 20, mock_win)
        cell.left_line.draw = MagicMock()
        cell.right_line.draw = MagicMock()
        cell.top_line.draw = MagicMock()
        cell.bottom_line.draw = MagicMock()

        cell.del_top()
        cell.draw()

        cell.left_line.draw.assert_called_once()
        cell.right_line.draw.assert_called_once()
        cell.top_line.draw.assert_called_once_with(cell.win.canvas, cell.bg_color)
        cell.bottom_line.draw.assert_called_once()

    def test_delete_bottom(self):
        mock_canvas = MagicMock()
        mock_win = MagicMock()
        mock_win.canvas = mock_canvas
        cell = Cell(10, 10, 20, 20, mock_win)
        cell.left_line.draw = MagicMock()
        cell.right_line.draw = MagicMock()
        cell.top_line.draw = MagicMock()
        cell.bottom_line.draw = MagicMock()

        cell.del_bot()
        cell.draw()

        cell.left_line.draw.assert_called_once()
        cell.right_line.draw.assert_called_once()
        cell.top_line.draw.assert_called_once()
        cell.bottom_line.draw.assert_called_once_with(cell.win.canvas, cell.bg_color)
    #CELL DRAW MOVE LINE TRACE DRAWING
    def test_draw_move(self):
        mock_canvas = MagicMock()
        mock_win = MagicMock()
        mock_win.canvas = mock_canvas

        cellA = Cell(10, 10, 20, 20, mock_win)
        cellB = Cell(20, 10, 30, 20, mock_win)

        with patch.object(Line, "draw") as mock_draw:
            cellA.draw_move(cellB)
            mock_draw.assert_called_once_with(mock_canvas, cellA.draw_color)

    def test_draw_move_undo(self):
        mock_canvas = MagicMock()
        mock_win = MagicMock()
        mock_win.canvas = mock_canvas

        cellA = Cell(10, 10, 20, 20, mock_win)
        cellB = Cell(20, 10, 30, 20, mock_win)

        with patch.object(Line, "draw") as mock_draw:
            cellB.draw_move(cellA, True)
            mock_draw.assert_called_once_with(mock_canvas, "gray")
    #INTERCEPT AND TEST POINTS FOR DRAW MOVE AT MIDPOINTS
    def test_draw_move_midpoint(self):
        mock_canvas = MagicMock()
        mock_win = MagicMock()
        mock_win.canvas = mock_canvas

        cellA = Cell(10, 10, 20, 20, mock_win)
        cellB = Cell(20, 10, 30, 20, mock_win)

        with patch("maze.Line") as MockLine:
            mock_line = MagicMock()
            MockLine.return_value = mock_line
            
            cellA.draw_move(cellB)

            args, kwargs = MockLine.call_args
            start_point = args[0]
            end_point = args[1]

            self.assertEqual(start_point.x, 15)
            self.assertEqual(start_point.y, 15)
            self.assertEqual(end_point.x, 25)
            self.assertEqual(end_point.y, 15)

    def test_draw_move_midpoint_rounding(self):
        mock_canvas = MagicMock()
        mock_win = MagicMock()
        mock_win.canvas = mock_canvas
        
        cellA = Cell(15, 15, 30, 30, mock_win)
        cellB = Cell(25, 15, 40, 30, mock_win)

        with patch("maze.Line") as MockLine:
            mock_line = MagicMock()
            MockLine.return_value = mock_line

            cellA.draw_move(cellB)

            args, kwargs = MockLine.call_args
            start = args[0]
            end = args[1]

            self.assertEqual(start.x, 22)
            self.assertEqual(start.y, 22)
            self.assertEqual(end.x, 32)
            self.assertEqual(end.y, 22)
    #MAZE FUNCTION TESTING
    @patch.object(Maze, "_animate", return_value=None)
    def test_maze_row_col_calculate(self, _):
        mock_canvas = MagicMock()
        mock_win = MagicMock()
        mock_win.canvas = mock_canvas
        mock_win.width = 800
        mock_win.height = 600

        maze = Maze(25, 25, 50, 50, None, mock_win)
        self.assertEqual(maze.width, 15)
        self.assertEqual(maze.height, 11)

   # @patch.object(Maze, "_break_entrance_and_exit", return_value=None)
    def test_maze_animation_call(self):
        mock_canvas = MagicMock()
        mock_win = MagicMock()
        mock_win.canvas = mock_canvas
        mock_win.width = 800
        mock_win.height = 600
        with patch.object(Maze, "_animate") as mock_animate:
            maze = Maze(25, 25, 50, 50, None, mock_win)
            self.assertEqual(mock_animate.call_count, maze.width * maze.height) 

    def test_maze_zero_values(self):
        with self.assertRaises(ValueError):
            maze = Maze(0, 0, 0, 0, None)

    def test_maze_doesnt_fit_width(self):
        mock_canvas = MagicMock()
        mock_win = MagicMock()
        mock_win.canvas = mock_canvas
        mock_win.width = 8
        mock_win.height = 100

        with self.assertRaises(ValueError):
            maze = Maze(10, 10, 50, 50, None, mock_win)

    def test_maze_doesnt_fit_height(self):
        mock_canvas = MagicMock()
        mock_win = MagicMock()
        mock_win.canvas = mock_canvas
        mock_win.width = 100
        mock_win.height = 8
        
        with self.assertRaises(ValueError):
            maze = Maze(10, 10, 50, 50, None, mock_win)

    def test_given_to_many_cols(self):
        mock_canvas = MagicMock()
        mock_win = MagicMock()
        mock_win.canvas = mock_canvas
        mock_win.width = 100
        mock_win.height = 100

        with self.assertRaises(ValueError):
            maze = Maze(10, 10, 50, 50, None, mock_win, 10, 10)

class QuadLinkCells(unittest.TestCase):
    def test_3x3(self):
        cols_rows = 3    
        maze = Maze(10, 10, 50, 50, None, None, cols_rows, cols_rows)
        current = maze.cells[0][0]
        self.assertEqual(current.left, None)
        self.assertEqual(current.right, maze.cells[1][0])
        self.assertEqual(current.up, None)
        self.assertEqual(current.down, maze.cells[0][1])
        current = current.right
        self.assertEqual(current.left, maze.cells[0][0])
        self.assertEqual(current.right, maze.cells[2][0])
        self.assertEqual(current.up, None)
        self.assertEqual(current.down, maze.cells[1][1])
        current = current.right
        self.assertEqual(current.left, maze.cells[1][0])
        self.assertEqual(current.right, None)
        self.assertEqual(current.up, None)
        self.assertEqual(current.down, maze.cells[2][1])
        current = current.down
        self.assertEqual(current.left, maze.cells[1][1])
        self.assertEqual(current.right, None)
        self.assertEqual(current.up, maze.cells[2][0])
        self.assertEqual(current.down, maze.cells[2][2])
        current = current.left
        self.assertEqual(current.left, maze.cells[0][1])
        self.assertEqual(current.right, maze.cells[2][1])
        self.assertEqual(current.up, maze.cells[1][0])
        self.assertEqual(current.down, maze.cells[1][2])
        current = current.left
        self.assertEqual(current.left, None)
        self.assertEqual(current.right, maze.cells[1][1])
        self.assertEqual(current.up, maze.cells[0][0])
        self.assertEqual(current.down, maze.cells[0][2])
        current = current.down
        self.assertEqual(current.left, None)
        self.assertEqual(current.right, maze.cells[1][2])
        self.assertEqual(current.up, maze.cells[0][1])
        self.assertEqual(current.down, None)
        current = current.right
        self.assertEqual(current.left, maze.cells[0][2])
        self.assertEqual(current.right, maze.cells[2][2])
        self.assertEqual(current.up, maze.cells[1][1])
        self.assertEqual(current.down, None)
        current = current.right
        self.assertEqual(current.left, maze.cells[1][2])
        self.assertEqual(current.right, None)
        self.assertEqual(current.up, maze.cells[2][1])
        self.assertEqual(current.down, None)
    
    def test_xy_index_value(self):
        cols_rows = 3    
        maze = Maze(10, 10, 50, 50, None, None, cols_rows, cols_rows)
        current = maze.cells[0][0]
        self.assertEqual(current.x_index, 0)
        self.assertEqual(current.y_index, 0)
        current = current.right
        current = current.down
        self.assertEqual(current.x_index, 1)
        self.assertEqual(current.y_index, 1)
        current = current.right
        current = current.down
        self.assertEqual(current.x_index, 2)
        self.assertEqual(current.y_index, 2)

    def test_grid_integrity(self):
        cols_rows = 3
        maze = Maze(10, 10, 50, 50, None, None, cols_rows, cols_rows)
        current = maze.cells[0][0]
        while current.right is not None:
            if current.left is not None:
                self.assertEqual(current.left.right, current)
            current = current.right
        while current.down is not None:
            if current.up is not None:
                self.assertEqual(current.up.down, current)
            current = current.down
        while current.left is not None:
            if current.right is not None:
                self.assertEqual(current.right.left, current)
            current = current.left
        while current.up is not None:
            if current.down is not None:
                self.assertEqual(current.down.up, current)
            current = current.up

        current = maze.cells[1][1]
        self.assertEqual(current.left.right, current)
        self.assertEqual(current.right.left, current)
        self.assertEqual(current.up.down, current)
        self.assertEqual(current.down.up, current)
        self.assertEqual(current.left.right.right, current.right)
        self.assertEqual(current.right.left.left, current.left)
        self.assertEqual(current.up.down.down, current.down)
        self.assertEqual(current.down.up.up, current.up)

    def test_vert_sparsity(self):
        maze = Maze(10, 10, 50, 50, None, None, 5, 1)
        current = maze.cells[0][0]
        self.assertEqual(current.up, None)
        while current.down is not None:
            self.assertEqual(current.left, None)
            self.assertEqual(current.right, None)
            current = current.down
        self.assertEqual(current.down, None)
        self.assertEqual(current, maze.cells[0][4])

    def test_horz_sparsity(self):
        maze = Maze(10, 10, 50, 50, None, None, 1, 5)
        current = maze.cells[0][0]
        self.assertEqual(current.left, None)
        while current.right is not None:
            self.assertEqual(current.up, None)
            self.assertEqual(current.down, None)
            current = current.right
        self.assertEqual(current.right, None)
        self.assertEqual(current, maze.cells[4][0])

    def test_minimal_maze(self):
        #a maze so simple it practically solves itself.....
        maze = Maze(10, 10, 50, 50, None, None, 1, 1)
        current = maze.cells[0][0]
        self.assertIsNone(current.right)
        self.assertIsNone(current.left)
        self.assertIsNone(current.up)
        self.assertIsNone(current.down)

    def test_deep_integrity(self):
        maze = Maze(10, 10, 50, 50, None, None, 5, 5)
        current = maze.cells[0][0]
        current = current.right
        current = current.down
        current = current.down
        current = current.right
        current = current.right
        self.assertEqual(current.left.left.up.up.left.right.down.down.right.right, current)

class GeneratorTests(unittest.TestCase):
    #manual parameterize since calling @patch before init for method captures
    #and parameterize can't easily wrap the patch decorators..... 
    #@patch.object(Maze, "_draw_cells")
    #@patch.object(Maze, "_animate")
    #@patch.object(Maze, "_reset_visited")
    #@parameterized.expand([
    #    ("recursive", "dfs_r"),
    #    ("stack", "dfs"),
    #])
    #def test_every_cell_visited(self, label, gen_key,  mock_reset, mock_animate, mock_draw):

    #THIS FAILS.
    
    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    @patch.object(Maze, "_reset_visited")
    def test_every_cell_visited_kruskal(self, *_):
        maze = Maze(10, 10, 50, 50, generators["kruskal"], None, 4, 4)
        group_id = maze.cells[0][0].group_id
        for col in maze.cells:
            for cell in col:
                self.assertEqual(cell.group_id, group_id)

    def _test_every_cell_visited(self, gen_key):
        maze = Maze(10, 10, 50, 50, generators[gen_key], None, 3, 3)
        for col in maze.cells:
            for cell in col:
                self.assertTrue(cell.visited)

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    @patch.object(Maze, "_reset_visited")
    def test_every_cell_visited_wilson(self, *_):
        self._test_every_cell_visited("wilson")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    @patch.object(Maze, "_reset_visited")
    def test_every_cell_visited_prim(self, *_):
        self._test_every_cell_visited("prim")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    @patch.object(Maze, "_reset_visited")
    def test_every_cell_visited_recursive(self, *_):
        self._test_every_cell_visited("dfs_r")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    @patch.object(Maze, "_reset_visited")
    def test_every_cell_visited_stack(self, *_):
        self._test_every_cell_visited("dfs")

    def _test_entrance(self, gen_key): 
        maze = Maze(10, 10, 50, 50, generators[gen_key], None, 3, 3)
        maze._draw_cells = MagicMock()
        ent_node = maze.cells[0][0]
        exit_node = maze.cells[2][2]
        self.assertEqual(ent_node.top_wall, False)
        self.assertEqual(exit_node.bottom_wall, False)

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_entrance_DFS_recursive(self, mock_animate, mock_draw):
        self._test_entrance("dfs_r")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_entrance_DFS_stack(self, mock_animate, mock_draw):
        self._test_entrance("dfs_r")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_entrance_prim(self, *_):
        self._test_entrance("prim")
    
    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_entrance_kruskal(self, *_):
        self._test_entrance("kruskal")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_entrance_wilson(self, *_):
        self._test_entrance("wilson")

    def _test_unvisit_after(self, gen_key):
        maze = Maze(10, 10, 50, 50, generators[gen_key], None, 3, 3)
        for col in maze.cells:
            for cell in col:
                self.assertFalse(cell.visited)

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_unvisit_after_DFS(self, mock_animate, mock_draw):
        self._test_unvisit_after("dfs_r")
        
    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_unvisit_after_DFS_stack(self, mock_animate, mock_draw):
        self._test_unvisit_after("dfs") 

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_unvisit_after_prim(self, *_):
        self._test_unvisit_after("prim")
        
    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_unvisit_after_wilson(self, *_):
        self._test_unvisit_after("wilson")

    #kruskal doesn't touch cell.visited

    def _test_no_unbroken_walls_between(self, gen_key):
        maze = Maze(10, 10, 50, 50, generators[gen_key], None, 3, 3)
        for col in maze.cells:
            for cell in col:
                if cell.left_wall == False:
                    self.assertFalse(cell.left.right_wall)
                if cell.right_wall == False:
                    self.assertFalse(cell.right.left_wall)
                if cell.top_wall == False and cell.y_index != 0:
                    self.assertFalse(cell.up.bottom_wall)
                if cell.bottom_wall == False and cell.y_index != 2:
                    self.assertFalse(cell.down.top_wall)

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_no_unbroken_walls_between_recursive(self, mock_animate, mock_draw):
        self._test_no_unbroken_walls_between("dfs_r")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_no_unbroken_walls_between(self, mock_animate, mock_draw):
        self._test_no_unbroken_walls_between("dfs")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_no_unbroken_walls_between_prim(self, *_):
        self._test_no_unbroken_walls_between("prim")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_no_unbroken_walls_between_kruskal(self, *_):
        self._test_no_unbroken_walls_between("kruskal")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_no_unbroken_walls_between_wilson(self, mock_animate, mock_draw):
        self._test_no_unbroken_walls_between("wilson")
    
    def _test_maze_sig_with_seed(self, gen_key):
        maze1 = Maze(10, 10, 50, 50, generators[gen_key], None, 5, 5, 1234)
        maze2 = Maze(10, 10, 50, 50, generators[gen_key], None, 5, 5, 1234)
        sig1, sig2 = [], []
        for col in maze1.cells:
            for cell in col:
                if cell.left_wall == False:
                    sig1.append("l")
                if cell.right_wall == False:
                    sig1.append("r")
                if cell.top_wall == False:
                    sig1.append("t")
                if cell.bottom_wall == False:
                    sig1.append("b")

        for col in maze2.cells:
            for cell in col:
                if cell.left_wall == False:
                    sig2.append("l")
                if cell.right_wall == False:
                    sig2.append("r")
                if cell.top_wall == False:
                    sig2.append("t")
                if cell.bottom_wall == False:
                    sig2.append("b")

        self.assertEqual(sig1, sig2)

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_maze_signatures_with_seed_recursive(self, mock_animate, mock_draw):
        self._test_maze_sig_with_seed("dfs_r")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_maze_signatures_with_seed_stack(self, mock_animate, mock_draw):
        self._test_maze_sig_with_seed("dfs")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_maze_sig_with_seed_prim(self, *_):
        self._test_maze_sig_with_seed("prim")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_maze_sig_with_seed_kruskal(self, *_):
        self._test_maze_sig_with_seed("kruskal")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_maze_sig_with_seed_wilson(self, *_):
        self._test_maze_sig_with_seed("wilson")
    
    def _test_maze_sig_different(self, gen_key):
        maze1 = Maze(10, 10, 50, 50, generators[gen_key], None, 20, 20, 1234)
        maze2 = Maze(10, 10, 50, 50, generators[gen_key], None, 20, 20, 4467)
        sig1, sig2 = [], []
        for col in maze1.cells:
            for cell in col:
                sig1.append(cell.x_index)
                sig1.append(cell.y_index)
                if cell.left_wall == False:
                    sig1.append("l")
                if cell.right_wall == False:
                    sig1.append("r")
                if cell.top_wall == False:
                    sig1.append("t")
                if cell.bottom_wall == False:
                    sig1.append("b")

        for col in maze2.cells:
            for cell in col:
                sig2.append(cell.x_index)
                sig2.append(cell.y_index)
                if cell.left_wall == False:
                    sig2.append("l")
                if cell.right_wall == False:
                    sig2.append("r")
                if cell.top_wall == False:
                    sig2.append("t")
                if cell.bottom_wall == False:
                    sig2.append("b")

        self.assertNotEqual(sig1, sig2)

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_maze_signatures_different_recursive(self, mock_animate, mock_draw):
        self._test_maze_sig_different("dfs_r")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_maze_signatures_different_recursive(self, mock_animate, mock_draw):
        self._test_maze_sig_different("dfs")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_maze_sig_differs_prim(self, *_):
        self._test_maze_sig_different("prim")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_maze_sig_differs_kruskal(self, *_):
        self._test_maze_sig_different("kruskal")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    def test_maze_sig_differs_wilson(self, *_):
        self._test_maze_sig_different("wilson")

class SolverTests(unittest.TestCase):
    
    def _test_solver_reaches_end(self, solve_key):
        maze = Maze(10, 10, 50, 50, generators["wilson"], None, 5, 5)
        maze.solve(solvers[solve_key])
        self.assertTrue(maze.cells[maze.width - 1][maze.height - 1].visited)

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    @patch.object(Cell, "draw_move")
    def test_solve_reaches_end_dfs(self, *_):
        self._test_solver_reaches_end("dfs")

    @patch.object(Maze, "_draw_cells")
    @patch.object(Maze, "_animate")
    @patch.object(Cell, "draw_move")
    def test_solver_reaches_end_dfs_r(self, *_):
        self._test_solver_reaches_end("dfs_r")

if __name__ == "__main__":
    unittest.main()
