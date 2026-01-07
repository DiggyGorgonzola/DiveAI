import math, random, time

class DIVE():
    grid,score,changed,name,seeds=None,None,None,None,None
    def __init__(self, grid=[
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ], score=0, changed=False, name="DIVE_Object", seeds=[]):
        self.grid=grid
        self.score=score
        self.changed=changed
        self.name = name
        self.seeds = seeds
    def __repr__(self):
        return self.grid

    def pretty_print(grid):
        RED = '\033[31m'
        GREEN = '\033[32m'
        CYAN = '\033[36m'
        RESET = '\033[0m'
        for i in range(4):
            for j in range(4):
                if grid[i][j] == 0:
                    print(RED + str(grid[i][j]) + RESET, end=", ")
                else:
                    print(CYAN + str(grid[i][j]) + RESET, end=", ")
            print("\n")
        return grid
    def self_pp(self):
        print("\n-------------")
        print(f"{self.name}'s current grid:")
        DIVE.pretty_print(self.grid)
        print("SCORE:",self.score)
        print("CURRENT SEEDS:",self.seeds)
        print("-------------\n")
        return self
    
    '''Movement logic methods'''
    def merges(a,b):
        return (True,min(a,b)) if math.gcd(a,b) in [a,b] else (False,0)
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
        new_grid, changed3, new_score2 = DIVE.merge_grid(new_grid)
        changed = changed1 or changed2 or changed3
        new_grid = DIVE.compress_grid(new_grid)[0]
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
    def move(self, move="l"):
        a = {
            "l":DIVE.move_left(self.grid),
            "r":DIVE.move_right(self.grid),
            "u":DIVE.move_up(self.grid),
            "d":DIVE.move_down(self.grid)
        }[move]
        self.grid, changed = a[0], a[1]
        self.score += a[2]
        return self
    
    '''other stuff'''
    def get_zeros(grid):
        # REMEMBER THAT POS IS (y,x)
        pos = []
        for i in range(4):
            for j in range(4):
                if grid[i][j] == 0:
                    pos.append((i,j))
        return pos
    def add_new_tile(grid, new_tile=2):
        position = random.choice(DIVE.get_zeros(grid))
        grid[position[0]][position[1]] = new_tile
        return grid
    def reset_grid(self):
        self.grid = DIVE.add_new_tile(DIVE.add_new_tile([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]))
        return self
    def get_new_seeds(grid, current_seeds):
        new_seeds = []
        for i in current_seeds:
            for j in range(4):
                for k in range(4):
                    if grid[j][k] % i == 0 and grid[j][k] != 0:
                        if i not in new_seeds and i != 1:
                            new_seeds.append(i)
                        if grid[j][k]//i not in new_seeds and grid[j][k]//i != 1:
                            new_seeds.append(grid[j][k]//i)
        return new_seeds
    def user_play(self, wasd_mode=True):
        while len(DIVE.get_zeros(self.grid)) > 0:
            if not wasd_mode:
                while (x:=input()) not in ["l","r","u","d"]:
                    pass
                self.move(x)
                self.seeds = DIVE.get_new_seeds(self.grid,self.seeds)
                DIVE.add_new_tile(self.grid, random.choice(self.seeds))
                self.self_pp()
            else:
                while (x:=input()) not in ["w","a","s","d"]:
                    pass
                self.move({"w":"u","a":"l","s":"d","d":"r"}[x])
                self.seeds = DIVE.get_new_seeds(self.grid,self.seeds)
                DIVE.add_new_tile(self.grid, random.choice(self.seeds))
                self.self_pp()

'''-=- testing zone ^w^ -=-'''
arr = [
        [4,2,4,2],
        [0,0,0,4],
        [0,0,0,2],
        [0,0,0,4]
    ]
A = DIVE(grid=arr, name="DIVE hehe", seeds=[2])
A.self_pp()
A.user_play()
