def _fast_find_neighbors(current):
    return [n for n in (current.left, current.right, current.up, current.down) if n is not None]

def _find_neighbors(current):
    neighbors = []
    if current.left is not None:
        neighbors.append(current.left)
    if current.right is not None:
        neighbors.append(current.right)
    if current.up is not None:
        neighbors.append(current.up)
    if current.down is not None:
        neighbors.append(current.down)

    return neighbors

def _solve_r(maze, current, end_cell):
    maze._animate()
    current.visited = True
    if current == end_cell:
        return True
    neighbors = _fast_find_neighbors(current)
    for neighbor in neighbors:
        if current.left == neighbor and not neighbor.right_wall and not neighbor.visited:
            current.draw_move(neighbor)
            if _solve_r(maze, neighbor, end_cell):
                return True
            else:
                current.draw_move(neighbor, True)
        
        if current.right == neighbor and not neighbor.left_wall and not neighbor.visited:
            current.draw_move(neighbor)
            if _solve_r(maze, neighbor, end_cell):
                return True
            else:
                current.draw_move(neighbor, True)
        
        if current.up == neighbor and not neighbor.bottom_wall and not neighbor.visited:
            current.draw_move(neighbor)
            if _solve_r(maze, neighbor, end_cell):
                return True
            else:
                current.draw_move(neighbor, True)
        
        if current.down == neighbor and not neighbor.top_wall and not neighbor.visited:
            current.draw_move(neighbor)
            if _solve_r(maze, neighbor, end_cell):
                return True
            else:
                current.draw_move(neighbor, True)

    return False
        

def dfs_r_solver(maze):
    end_cell = maze.cells[maze.width - 1][maze.height - 1]
    start_cell = maze.cells[0][0]
    _solve_r(maze, start_cell, end_cell) 

def bfs_solver(maze):
    pass

def dijkstra_solver(maze):
    pass

def a_star_solver(maze):
    pass

def best_first_solver(maze):
    pass

def recurse_backtrack_solver(maze):
    pass

def bidirectional_solver(maze):
    pass

def left_hand_solver(maze):
    pass

def dead_end_fill_solver(maze):
    pass

solvers = {
        "dfs_r" : dfs_r_solver,
        "bfs" : bfs_solver,
        "dijk" : dijkstra_solver,
        "a_star" : a_star_solver,
        "best_f" : best_first_solver,
        "r_back" : recurse_backtrack_solver,
        "bidir" : bidirectional_solver,
        "lefthand" : left_hand_solver,
        "dead" : dead_end_fill_solver,
        }
