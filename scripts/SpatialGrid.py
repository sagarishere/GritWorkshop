class SpatialGrid:
    def __init__(self, width, height, cell_size):
        self.cell_size = cell_size
        self.cols = width // cell_size
        self.rows = height // cell_size
        self.grid = [[[] for _ in range(self.cols)] for _ in range(self.rows)]
        
    def insert(self, obj):
        col, row = int(obj.x // self.cell_size), int(obj.y // self.cell_size)
        self.grid[row][col].append(obj)
        
    def get_neighboring_objects(self, x, y):
        col, row = int(x // self.cell_size), int(y // self.cell_size)
        neighbors = []
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_col, new_row = col + j, row + i
                if 0 <= new_col < self.cols and 0 <= new_row < self.rows:
                    neighbors.extend(self.grid[new_row][new_col])
                    
        return neighbors
