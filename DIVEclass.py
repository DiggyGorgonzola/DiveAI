import math, random, time

class DIVE():
    grid,score,changed = None,None,None
    def __init__(self, grid=[
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ], score=0, changed=False):
        self.grid = grid
        self.score=score
        self.changed=changed
    def pretty_print(grid):
        for i in range(4):
            for j in range(4):
                print(grid[i][j], end=", ")
            print("\n")
    def __repr__(self):
        return self.grid
    def self_pp(self):
        DIVE.pretty_print(self.grid)
    '''AI methods'''
    def merges(a,b):
        return (True,min(a,b)) if math.gcd(a,b) in [a,b] else (False,0)
    
    '''Movement logic methods'''
    def compress_grid(grid):
        changed = False
        new_grid = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
        for i in range(4):
            pos = 0
            for j in range(4):
                if grid[i][j] != 0:
                    new_grid[i][pos] = grid[i][j]
                    if j != pos:
                        changed = True
                    pos += 1
        return new_grid, changed
    def merge_grid(grid):
        changed = False
        add_score = 0
        for i in range(4):
            for j in range(3):
                if DIVE.merges(grid[i][j], grid[i][j+1])[0]:
                    add_score += DIVE.merges(grid[i][j], grid[i][j+1])[1]
                    grid[i][j] = grid[i][j] + grid[i][j+1]
                    grid[i][j+1] = 0
                    changed = True
        return grid, changed, add_score
    def reverse_grid(grid):
        new_grid = []
        for i in range(4):
            new_grid.append([])
            for j in range(4):
                new_grid[i].append(grid[i][3-j])
        return new_grid
    def transpose_grid(grid):
        new_grid = []
        for i in range(4):
            new_grid.append([])
            for j in range(4):
                new_grid[i].append(grid[j][i])
        return new_grid
    
    def move_left(grid):
        new_grid, changed1 = DIVE.compress_grid(grid)
        new_grid, changed2, new_score = DIVE.merge_grid(new_grid)
        changed = changed1 or changed2
        new_grid, temp = DIVE.compress_grid(new_grid)
        new_grid, temp, new_score2 = DIVE.merge_grid(new_grid)
        return new_grid, changed, new_score + new_score2
    def move_right(grid):
        new_grid = DIVE.reverse_grid(grid)
        new_grid, changed, new_score = DIVE.move_left(new_grid)
        new_grid = DIVE.reverse_grid(new_grid)
        return new_grid, changed, new_score
    def move_up(grid):
        new_grid = DIVE.transpose_grid(grid)
        new_grid, changed, new_score = DIVE.move_left(new_grid)
        new_grid = DIVE.transpose_grid(new_grid)
        return new_grid, changed, new_score
    def move_down(grid):
        new_grid = DIVE.transpose_grid(grid)
        new_grid, changed, new_score = DIVE.move_right(new_grid)
        new_grid = DIVE.transpose_grid(new_grid)
        return new_grid, changed, new_score

    '''untested shiz'''
    def move(self, move="l"):
        a = {
            "l":DIVE.move_left(self.grid)
            "r":DIVE.move_right(self.grid)
            "u":DIVE.move_up(self.grid)
            "d":DIVE.move_down(self.grid)
        }[move]
        self.grid, changed = a[0], a[1]
        self.score += a[2]
    def get_pos_zeros(grid):
        # REMEMBER THAT POS IS (y,x)
        pos = []
        for i in range(4):
            for j in range(4):
                if grid[i][j] = 0:
                    pos.append((i,j))
        return pos
    def add_new_tile(grid, new_tile=2):
        position = random.choice(DIVE.get_pos_zeros(grid))
        grid[position[0]][position[1]] = new_tile
        return grid
    def reset_grid(self):
        self.grid = DIVE.add_new_tile(DIVE.add_new_tile([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]))
'''-=- testing zone ^w^ -=-'''
arr = [
        [4,2,4,2],
        [0,0,0,4],
        [0,0,0,2],
        [0,0,0,4]
    ]
A = DIVE(grid=arr)
DIVE.pretty_print(DIVE.move_up(A.grid)[0])
