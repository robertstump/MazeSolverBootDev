import random

def _break_ent_ext(maze, current, exit_node):
    current.del_top()
    exit_node.del_bot()

    if maze.win is not None:
        maze._draw_cells(current.x_index, current.y_index)
        maze._draw_cells(exit_node.x_index, exit_node.y_index)


def _find_neighbors(maze, current):
    to_visit = []
    if current.left is not None and current.left.visited is False:
        to_visit.append(current.left)
    if current.right is not None and current.right.visited is False:
        to_visit.append(current.right)
    if current.up is not None and current.up.visited is False:
        to_visit.append(current.up)
    if current.down is not None and current.down.visited is False:
        to_visit.append(current.down)
    
    return to_visit

def _break_sibling_walls(current, next_node):
    if next_node is current.left:
        current.del_left()
        next_node.del_right()
    elif next_node is current.right:
        current.del_right()
        next_node.del_left()
    elif next_node is current.up:
        current.del_top()
        next_node.del_bot()
    elif next_node is current.down:
        current.del_bot()
        next_node.del_top()

def _break_walls_DFS(maze, current):
    current.visited = True
    to_visit = []
    to_visit.append(current)
    current.visited = True
    
    while to_visit:
        current = to_visit[-1]
        neighbors = _find_neighbors(maze, current)
        #random.shuffle(neighbors)
        
        if neighbors:
            new_direction = maze.rng.randint(0, len(neighbors) - 1)
            next_node = neighbors[new_direction]
            to_visit.append(next_node)
            next_node.visited = True

            _break_sibling_walls(current, next_node)
            maze._draw_cells(current.x_index, current.y_index)
            maze._draw_cells(next_node.x_index, next_node.y_index)

        if not neighbors:
            current = to_visit.pop()
            maze._draw_cells(current.x_index, current.y_index)

def _break_walls_DFS_r(maze, current):
    current.visited = True

    while True:
        to_visit = _find_neighbors(maze, current)

        if not to_visit:
            maze._draw_cells(current.x_index, current.y_index)
            break

        new_direction = maze.rng.randint(0, len(to_visit) - 1)
        next_node = to_visit[new_direction]
        del to_visit[new_direction]

        _break_sibling_walls(current, next_node)
        maze._draw_cells(current.x_index, current.y_index)
        maze._draw_cells(next_node.x_index, next_node.y_index)

        _break_walls_DFS_r(maze, next_node)
        
def non_recursive_DFS(maze):
    current = maze.cells[0][0]
    exit_node = maze.cells[maze.width - 1][maze.height - 1]
    _break_ent_ext(maze, current, exit_node) 
    _break_walls_DFS(maze, current)

def randomized_DFS(maze):
    current = maze.cells[0][0]
    exit_node = maze.cells[maze.width - 1][maze.height - 1]
    _break_ent_ext(maze, current, exit_node)
    _break_walls_DFS_r(maze, current)
        
def prim_algorithm(maze):
    current = maze.cells[0][0]
    exit_node = maze.cells[maze.width - 1][maze.height - 1]
    _break_ent_ext(maze, current, exit_node)

    frontier = []
    neighbors = _find_neighbors(maze, current)
    for neighbor in neighbors:
        frontier.append((current, neighbor))
    while frontier:
        random.shuffle(frontier)

        next_node = frontier[0]
        del frontier[0]
        if next_node[1].visited == False:
            next_node[1].visited = True
            _break_sibling_walls(next_node[0], next_node[1])
            maze._draw_cells(next_node[0].x_index, next_node[0].y_index)
            maze._draw_cells(next_node[1].x_index, next_node[1].y_index)
        neighbors = _find_neighbors(maze, next_node[1])
        for neighbor in neighbors:
            frontier.append((next_node[1], neighbor))

def krusk_find(cell):
    return cell.group_id

def krusk_union(maze, cell_a, cell_b):
    old_id = cell_b.group_id
    new_id = cell_a.group_id

    for col in maze.cells:
        for cell in col:
            if cell.group_id == old_id:
                cell.group_id = new_id

def krusk_wall_finder(maze, current):
    walls = []
    if current.right is not None:
       walls.append((current, current.right))
    if current.down is not None: 
        walls.append((current, current.down))

    return walls


def kruskal_algorithm(maze):
    current = maze.cells[0][0]
    exit_node = maze.cells[maze.width - 1][maze.height - 1]
    _break_ent_ext(maze, current, exit_node)    

    next_list = []
    for col in maze.cells:
        for cell in col:
            next_list.extend(krusk_wall_finder(maze, cell))

    random.shuffle(next_list)
    while next_list:
        cell_a = next_list[0][0]
        cell_b = next_list[0][1]
        del next_list[0]

        if krusk_find(cell_a) != krusk_find(cell_b):
            _break_sibling_walls(cell_a, cell_b)
            maze._draw_cells(cell_a.x_index, cell_a.y_index)
            maze._draw_cells(cell_b.x_index, cell_b.y_index)
            krusk_union(maze, cell_a, cell_b)

def _wilson_find_neighbors(maze, current):
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

def _check_for_loop(path, next_node):
    if next_node in path: 
        while path[-1] is not next_node:
            del path[-1]

def _carve_path(maze, path):
    path_length = len(path)
    for x in range(1, path_length):
        _break_sibling_walls(path[x - 1], path[x])

    
def wilson_algorithm(maze):
    enter_node = maze.cells[0][0]
    exit_node = maze.cells[maze.width - 1][maze.height - 1]
    _break_ent_ext(maze, enter_node, exit_node) 
    enter_node.visited = True
  
    to_visit = []
    for col in maze.cells:
        for cell in col:
            to_visit.append(cell)
    to_visit.remove(enter_node)

    while to_visit:
        current = maze.rng.choice(to_visit)
        path = [current]
        walk_set = {current}
        #walking
        while True:
            neighbors = _wilson_find_neighbors(maze, current)
            next_node = maze.rng.choice(neighbors) 
            if next_node in walk_set:
                while path[-1] != next_node:
                    walk_set.remove(path.pop())
                current = next_node
                continue

            if next_node.visited is True:
                path.append(next_node)
                _carve_path(maze, path)
                for node in path:
                    maze._draw_cells(node.x_index, node.y_index)
                    node.visited = True
                    if node in to_visit:
                        to_visit.remove(node)
                break

            path.append(next_node)
            walk_set.add(next_node)
            current = next_node

def wilson_algorithm2(maze):
    start_cell = maze.cells[0][0]
    start_cell.visited = True

    unvisited = []
    for col in maze.cells:
        for cell in col:
            if not cell.visited:
                unvisited.append(cell)

    while unvisited:
        # Pick a random unvisited start point
        current = maze.rng.choice(unvisited)

        path = [current]
        visited_in_walk = {current}

        while True:
            neighbors = _wilson_find_neighbors(maze, current)
            next_node = maze.rng.choice(neighbors)

            if next_node in visited_in_walk:
                # Loop detected: erase back to first occurrence
                while path[-1] != next_node:
                    visited_in_walk.remove(path.pop())
                current = next_node
                continue

            path.append(next_node)

            if next_node.visited:
                # Hit the maze: carve the path
                _carve_path(maze, path)
                for cell in path:
                    if not cell.visited:
                        maze._draw_cells(cell.x_index, cell.y_index)
                        cell.visited = True
                        if cell in unvisited:
                            unvisited.remove(cell)
                break
            else:
                visited_in_walk.add(next_node)
                current = next_node

generators = {
        "dfs_r" : randomized_DFS,
        "dfs" : non_recursive_DFS,
        "prim" : prim_algorithm,
        "kruskal" : kruskal_algorithm,
        "wilson" : wilson_algorithm,
        "wilsonAI" :wilson_algorithm2
        }
