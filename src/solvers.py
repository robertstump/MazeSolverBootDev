import queue
from collections import deque

def _fast_find_neighbors(current):
    return [n for n in (current.left, current.right, current.up, current.down) if n is not None and n.visited == False]

def _find_neighbors(current):
    neighbors = []
    if current.up and not current.top_wall and not current.up.visited:
        neighbors.append(current.up)
    if current.right and not current.right_wall and not current.right.visited:
        neighbors.append(current.right)
    if current.down and not current.bottom_wall and not current.down.visited:
        neighbors.append(current.down)
    if current.left and not current.left_wall and not current.left.visited:
        neighbors.append(current.left)

    return neighbors

def _solve_r(maze, current, end_cell):
    maze._animate()
    current.visited = True
    if current == end_cell:
        return True
    neighbors = _fast_find_neighbors(current)
    for neighbor in neighbors:
        if current.left == neighbor and not neighbor.right_wall:
            current.draw_move(neighbor)
            if _solve_r(maze, neighbor, end_cell):
                return True
            else:
                current.draw_move(neighbor, True)
        
        if current.right == neighbor and not neighbor.left_wall:
            current.draw_move(neighbor)
            if _solve_r(maze, neighbor, end_cell):
                return True
            else:
                current.draw_move(neighbor, True)
        
        if current.up == neighbor and not neighbor.bottom_wall:
            current.draw_move(neighbor)
            if _solve_r(maze, neighbor, end_cell):
                return True
            else:
                current.draw_move(neighbor, True)
        
        if current.down == neighbor and not neighbor.top_wall:
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

def dfs_solver(maze):
    end_cell = maze.cells[maze.width - 1][maze.height - 1]
    start_cell = maze.cells[0][0]
    to_visit = [start_cell]
    while to_visit:
        maze._animate()
        current = to_visit[-1]

        current.visited = True
        if current == end_cell:
            return

        neighbors = _find_neighbors(current)
        if neighbors:
            neighbor = neighbors.pop()
            to_visit.append(neighbor)
            current.draw_move(neighbor)

        else: 
            current = to_visit.pop()
            if to_visit:
                to_visit[-1].draw_move(current, True)
        

def bfs_solver(maze):
    end_cell = maze.cells[maze.width - 1][maze.height - 1]
    start_cell = maze.cells[0][0]
    to_visit = [start_cell]
    while to_visit:
        maze._animate()
        current = to_visit[0]
        to_visit.remove(current)
        if current.parent is not None:
            current.draw_move(current.parent, True)

        current.visited = True
        if current == end_cell:
            while current.parent is not None:
                maze._animate()
                if current.parent is not start_cell:
                    current.draw_move(current.parent)
                    current = current.parent
                else: 
                    current.parent.draw_move(current) 
                    current = current.parent
            return

        neighbors = _find_neighbors(current)
        for neighbor in neighbors:
            neighbor.parent = current

        to_visit.extend(neighbors)

def dijkstra_solver(maze):
    end_cell = maze.cells[maze.width - 1][maze.height - 1]
    start_cell = maze.cells[0][0]
    priority_visit = queue.PriorityQueue()
    current_cost = 0
    counter = 0
    priority_visit.put((current_cost, counter, start_cell))

    while not priority_visit.empty():
        maze._animate()
        current_cost, _count, current = priority_visit.get()
        if current.parent is not None:
            current.draw_move(current.parent, True)

        current.visited = True
        if current == end_cell:
            while current.parent is not None:
                maze._animate()
                if current.parent is not start_cell:
                    current.draw_move(current.parent)
                    current = current.parent
                else:
                    current.parent.draw_move(current)
                    current = current.parent
            return

        neighbors = _find_neighbors(current)
        for neighbor in neighbors:
            counter += 1
            neighbor_cost = current_cost + 1
            neighbor.parent = current
            priority_visit.put((neighbor_cost, counter,  neighbor))

def _manhattan_to_goal(current, end_cell):
    return abs(current.x_index - end_cell.x_index) + abs(current.y_index - end_cell.y_index)

def a_star_solver(maze):
    end_cell = maze.cells[maze.width - 1][maze.height - 1]
    start_cell = maze.cells[0][0]
    priority_visit = queue.PriorityQueue()
    current_cost = 0
    estimate_cost = _manhattan_to_goal(start_cell, end_cell)
    counter = 0
    priority_visit.put((current_cost + estimate_cost, counter, start_cell))

    while not priority_visit.empty():
        maze._animate()
        current_cost, _count, current = priority_visit.get()
        if current.parent is not None:
            current.draw_move(current.parent, True)

        current.visited = True
        if current == end_cell:
            while current.parent is not None:
                maze._animate()
                if current.parent is not start_cell:
                    current.draw_move(current.parent)
                    current = current.parent
                else:
                    current.parent.draw_move(current)
                    current = current.parent
            return

        neighbors = _find_neighbors(current)
        for neighbor in neighbors:
            counter += 1
            estimate_cost = _manhattan_to_goal(neighbor, end_cell)
            neighbor_cost = current_cost + estimate_cost + 1
            neighbor.parent = current
            priority_visit.put((neighbor_cost, counter, neighbor))

def best_first_solver(maze):
    start_cell = maze.cells[0][0]
    end_cell = maze.cells[maze.width - 1][maze.height - 1]
    priority_visit = queue.PriorityQueue()
    estimate_cost = _manhattan_to_goal(start_cell, end_cell)
    counter = 0
    priority_visit.put((estimate_cost, counter, start_cell))

    while not priority_visit.empty():
        maze._animate()
        _estimate_cost, _counter, current = priority_visit.get()
        if current.parent is not None:
            current.parent.draw_move(current, True)

        current.visited = True
        if current == end_cell:
            while current.parent is not None:
                maze._animate()
                if current.parent is not start_cell:
                    current.draw_move(current.parent)
                    current = current.parent
                else:
                    current.parent.draw_move(current)
                    current = current.parent
            return

        neighbors = _find_neighbors(current)
        for neighbor in neighbors:
            neighbor.parent = current
            new_estimate = _manhattan_to_goal(neighbor, end_cell)
            counter += 1
            priority_visit.put((new_estimate, counter, neighbor))

def r_bt_solver(maze, current, end_cell):
    current.visited = True
    if current == end_cell:
        return True
    neighbors = _find_neighbors(current)
    for neighbor in neighbors:
        current.draw_move(neighbor)
        maze._animate()
        if r_bt_solver(maze, neighbor, end_cell):
            return True
        else:
            neighbor.draw_move(current, True)

    return False

def recurse_backtrack_solver(maze):
    start_cell = maze.cells[0][0]
    end_cell = maze.cells[maze.width - 1][maze.height -1]
    r_bt_solver(maze, start_cell, end_cell)

def _find_neighbors_end(current):
    neighbors = []
    if current.up and not current.top_wall and not current.up.end_visited:
        neighbors.append(current.up)
    if current.right and not current.right_wall and not current.right.end_visited:
        neighbors.append(current.right)
    if current.down and not current.bottom_wall and not current.down.end_visited:
        neighbors.append(current.down)
    if current.left and not current.left_wall and not current.left.end_visited:
        neighbors.append(current.left)

    return neighbors

def _path_retrace(maze, start_current, start_cell):
    while start_current.parent is not None:
        if start_current.parent is not start_cell:
            start_current.parent.draw_move(start_current)
            start_current = start_current.parent
        else: 
            start_cell.draw_move(start_current)
            start_current = start_current.parent

    maze._animate() 

def _path_retrace_end(maze, end_current, end_cell):
    while end_current.end_parent is not None:
        if end_current.end_parent is not end_cell:
            end_current.end_parent.draw_move(end_current)
            end_current = end_current.end_parent
        else:
            end_cell.draw_move(end_current)
            end_current = end_current.end_parent

    maze._animate()

def bidirectional_solver(maze):
    start_cell = maze.cells[0][0]    
    end_cell = maze.cells[maze.width - 1][maze.height - 1]
    start_visit = deque([start_cell])
    end_visit = deque([end_cell])
    meeting = None

    while start_visit and end_visit:
        start_current = start_visit.popleft()
        end_current = end_visit.popleft()
        if start_current.parent is not None:
            start_current.parent.draw_move(start_current, True)
        if end_current.end_parent is not None:
            end_current.end_parent.draw_move(end_current, True)

        start_current.visited = True
        end_current.end_visited = True
        
        start_neighbors = _find_neighbors(start_current)
        if start_neighbors:
            start_neighbor = start_neighbors[0]
            
        for neighbor in start_neighbors:
            if neighbor.end_visited:
                meeting = neighbor
                meeting.parent = start_current
                start_current = meeting
                end_current = meeting
                break
            else:
                neighbor.parent = start_current
        
        end_neighbors = _find_neighbors_end(end_current)
        if end_neighbors:
            end_neighbor = end_neighbors[0]

        for neighbor in end_neighbors:
            if neighbor.visited:
                meeting = neighbor
                meeting.end_parent = end_current
                end_current = meeting
                start_current = meeting
                break
            else:
                neighbor.end_parent = end_current
        
        if meeting is not None:
            _path_retrace_end(maze, end_current, end_cell)
            _path_retrace(maze, start_current, start_cell)
            return
        else:
            start_visit.extend(start_neighbors)
            end_visit.extend(end_neighbors)
        maze._animate()

def left_hand_solver(maze):
    current = maze.cells[0][0]
    end_cell = maze.cells[maze.width - 1][maze.height - 1]
    
    neighbors = _find_neighbors(current)
    if current.right in neighbors:
        facing = 1
    else:
        facing = 2

    while current is not end_cell:
        directions = [current.up, current.right, current.down, current.left]
        neighbors = _find_neighbors(current)
        #look left of facing
        left = (facing + 3) % 4
        right = (facing + 1) % 4
        back = (facing + 2) % 4

        if directions[left] in neighbors:
            current.draw_move(directions[left], False, "green")
            current = directions[left]
            facing = left
            maze._animate()
        elif directions[facing] in neighbors:
            current.draw_move(directions[facing])
            current = directions[facing]
            maze._animate()
        elif directions[right] in neighbors:
            current.draw_move(directions[right], False, "blue")
            current = directions[right]
            facing = right
            maze._animate()
        else:
            current.draw_move(directions[back], True)
            current = directions[back]
            facing = back
            maze._animate()

def dead_end_fill_solver(maze):
    #bring out your dead
    start_cell = maze.cells[0][0]
    end_cell = maze.cells[maze.width - 1][maze.height - 1]
    start_cell.up = end_cell
    end_cell.down = start_cell
    found_dead = True
    cell_set = set()
    for col in maze.cells:
        for cell in col:
            cell_set.add(cell)
    while found_dead:
        found_dead = False
        for cell in list(cell_set):
            neighbors = _find_neighbors(cell)
            maze._animate()
            #print(neighbors)
            if len(neighbors) == 1:
                found_dead = True
                cell.visited = True
                neighbor = neighbors[0]
                if neighbor == cell.up:
                    cell.top_wall = True
                    neighbor.bottom_wall = True
                    cell.draw_X()
                    cell_set.remove(cell)
                elif neighbor == cell.down:
                    cell.bottom_wall = True
                    neighbor.top_wall = True
                    cell.draw_X()
                    cell_set.remove(cell)
                elif neighbor == cell.right:
                    cell.right_wall = True
                    neighbor.left_wall = True
                    cell.draw_X()
                    cell_set.remove(cell)
                elif neighbor == cell.left:
                    cell.left_wall = True
                    neighbor.right_wall = True
                    cell.draw_X()
                    cell_set.remove(cell)

    start_cell.up = None
    end_cell.down = None
    current = start_cell
    while current is not end_cell:
        neighbors = _find_neighbors(current)
        if neighbors[0] is current.parent:
            neighbor = neighbors[1]
        else: 
            neighbor = neighbors[0] 

        current.draw_move(neighbor)
        maze._animate()
        neighbor.parent = current
        current = neighbor

solvers = {
        "dfs_r" : dfs_r_solver,
        "dfs" : dfs_solver,
        "bfs" : bfs_solver,
        "dijk" : dijkstra_solver,
        "a_star" : a_star_solver,
        "best_f" : best_first_solver,
        "r_back" : recurse_backtrack_solver,
        "bidir" : bidirectional_solver,
        "lefthand" : left_hand_solver,
        "dead" : dead_end_fill_solver,
        }
