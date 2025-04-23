import unittest
from unittest.mock import MagicMock, patch

from maze import Maze, Point, Line, Cell

class SetupTests(unittest.TestCase):
    #MAZE CREATION OVERALL WORKING
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, 10, 10, None, num_rows, num_cols) 
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
            mock_draw.assert_called_once_with(mock_canvas, "red")

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

        maze = Maze(25, 25, 50, 50, mock_win)
        self.assertEqual(maze.width, 15)
        self.assertEqual(maze.height, 11)

    @patch.object(Maze, "_break_entrance_and_exit", return_value=None)
    def test_maze_animation_call(self, _):
        mock_canvas = MagicMock()
        mock_win = MagicMock()
        mock_win.canvas = mock_canvas
        mock_win.width = 800
        mock_win.height = 600
        with patch.object(Maze, "_animate") as mock_animate:
            maze = Maze(25, 25, 50, 50, mock_win)
            self.assertEqual(mock_animate.call_count, maze.width * maze.height) 

    def test_maze_zero_values(self):
        with self.assertRaises(ValueError):
            maze = Maze(0, 0, 0, 0)

    def test_maze_doesnt_fit_width(self):
        mock_canvas = MagicMock()
        mock_win = MagicMock()
        mock_win.canvas = mock_canvas
        mock_win.width = 8
        mock_win.height = 100

        with self.assertRaises(ValueError):
            maze = Maze(10, 10, 50, 50, mock_win)

    def test_maze_doesnt_fit_height(self):
        mock_canvas = MagicMock()
        mock_win = MagicMock()
        mock_win.canvas = mock_canvas
        mock_win.width = 100
        mock_win.height = 8
        
        with self.assertRaises(ValueError):
            maze = Maze(10, 10, 50, 50, mock_win)

    def test_given_to_many_cols(self):
        mock_canvas = MagicMock()
        mock_win = MagicMock()
        mock_win.canvas = mock_canvas
        mock_win.width = 100
        mock_win.height = 100

        with self.assertRaises(ValueError):
            maze = Maze(10, 10, 50, 50, mock_win, 10, 10)
'''
class MazeBuilderTest(unittest.TestCase):
    def test_break_ent_exit(self):
        maze = Maze(10, 10, 50, 50, None, 10, 10)
        end_col = maze.width - 1
        end_row = maze.height - 1

        self.assertEqual(maze.cells[0][0].top_wall, False)
        self.assertEqual(maze.cells[end_row][end_col].bottom_wall, False)
'''
if __name__ == "__main__":
    unittest.main()
