import random

def _break_walls_r(maze, x, y):
    current = maze.cells[x][y]
    current.visited = True

    while True:
        to_visit = []
        if current.left is not None and current.left.visited is False:
            to_visit.append(current.left)
        if current.right is not None and current.right.visited is False:
            to_visit.append(current.right)
        if current.up is not None and current.up.visited is False:
            to_visit.append(current.up)
        if current.down is not None and current.down.visited is False:
            to_visit.append(current.down)

        if not to_visit: 
            maze._draw_cells(current.x_index, current.y_index)
            break

        new_direction = maze.rng.randint(0, len(to_visit) - 1)
        next = to_visit[new_direction]
        #del to_visit[new_direction]

        if next is current.left:
            current.del_left()
            next.del_right()
        elif next is current.right:
            current.del_right()
            next.del_left()
        elif next is current.up:
            current.del_top()
            next.del_bot()
        elif next is current.down:
            current.del_bot()
            next.del_top()

        maze._draw_cells(current.x_index, current.y_index)
        maze._draw_cells(next.x_index, next.y_index)

        _break_walls_r(maze, next.x_index, next.y_index)
        
        
def randomized_DFS(maze):
    #break start and end walls:
    current = maze.cells[0][0]
    exit_node = maze.cells[maze.width - 1][maze.height - 1]
    current.del_top()
    exit_node.del_bot()

    if maze.win is not None:
        maze._draw_cells(current.x_index, current.y_index) 
        maze._draw_cells(exit_node.x_index, exit_node.y_index)

    _break_walls_r(maze, current.x_index, current.y_index)
        
def prim_algorithm(maze):
    pass

def non_recursive_DFS(maz):
    pass

def prim_algorithm(maze):
    pass

def kruskal_algorithm(maze):
    pass

def wilson_algorithm(maze):
    pass

generators = {
        "dfs_r" : randomized_DFS,
        "dfs" : non_recursive_DFS,
        "prim" : prim_algorithm,
        "kruskal" : kruskal_algorithm,
        "wilson" : wilson_algorithm
        }
