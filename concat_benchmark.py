#courtesy of Jippity
import time, tracemalloc, gc

NUM_CELLS = 1000000

# Fake cell data generator
class FakeCell:
    def __init__(self, x, y):
        self.x_index = x
        self.y_index = y
        self.left_wall = False
        self.right_wall = True
        self.top_wall = False
        self.bottom_wall = True

cells = [FakeCell(i % 100, i // 100) for i in range(NUM_CELLS)]

print(f"Running benchmarks for {NUM_CELLS} cells...\n")
gc.disable()

# --- 1. String += concat ---
tracemalloc.start()
start = time.time()
sig = ""
for cell in cells:
    if not cell.left_wall:
        sig += f"{cell.x_index},{cell.y_index},l;"
    if not cell.top_wall:
        sig += f"{cell.x_index},{cell.y_index},t;"
end = time.time()
print(f"String '+=' concat time:     {end - start:.6f} seconds")
current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024:.2f} KB; Peak: {peak / 1024:.2f} KB")
tracemalloc.stop()

# --- 2. Append then join ---
tracemalloc.start()
start = time.time()
parts = []
for cell in cells:
    if not cell.left_wall:
        parts.append(f"{cell.x_index},{cell.y_index},l;")
    if not cell.top_wall:
        parts.append(f"{cell.x_index},{cell.y_index},t;")
sig = ''.join(parts)
end = time.time()
print(f"List append + join time:    {end - start:.6f} seconds")
current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024:.2f} KB; Peak: {peak / 1024:.2f} KB")


# --- 3. Raw list append (no join) ---
tracemalloc.start()
start = time.time()
raw = []
for cell in cells:
    if not cell.left_wall:
        raw.append(("l", cell.x_index, cell.y_index))
    if not cell.top_wall:
        raw.append(("t", cell.x_index, cell.y_index))
end = time.time()
print(f"Raw tuple list append time: {end - start:.6f} seconds")
current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024:.2f} KB; Peak: {peak / 1024:.2f} KB")
tracemalloc.stop()



