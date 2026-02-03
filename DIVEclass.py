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
        return f"{self.name}"
    def copy(self):
        return DIVE(
            grid=[row[:] for row in self.grid],
            changed=self.changed,
            score=self.score,
            seeds=self.seeds[:],
            name=self.name
        )
    def randomDive():
        return DIVE(
            grid=[[random.randrange(0,10) if random.random() < .5 else 0 for _ in range(4)] for he in range(4)],
            changed = False,
            score = 0,
            seeds = [2],
            name = "random dive object"
        )
    def listify(self):
        listifyy = []
        for i in range(4):
            for j in range(4):
                listifyy.append(self.grid[i][j])
        return listifyy 

    def get_prime_factors(n):
        facts = {5:0,3:0,2:0}
        for i in [5, 3, 2]:
            while n % i == 0 and n != 0:
                n //= i
                facts[i]+=1
        return facts
    def CUFOB(self):
        x = self.listify()
        g = 0
        for i in x:
            j = i
            n = 2
            while n <= i:
                if j % n == 0:
                    g += 1
                while j % n == 0:
                    j //= n
                n += 1
        return g
                 
    def pretty_print(grid):
        RED = '\033[31m'
        GREEN = '\033[32m'
        CYAN = '\033[36m'
        GREY = '\033[90m'
        LG = '\033[37m'
        RESET = '\033[0m'
        for i in range(4):
            for j in range(4):
                hehe = DIVE.get_prime_factors(grid[i][j])
                if grid[i][j] == 0:
                    print(GREY + str(grid[i][j]) + RESET, end=", ")
                elif hehe[2] == hehe[3] == hehe[5] == 0:
                    print(LG + str(grid[i][j]) + RESET, end=", ")
                elif max(hehe, key=hehe.get) == 5:
                    print(CYAN + str(grid[i][j]) + RESET, end=", ")
                elif max(hehe, key=hehe.get) == 3:
                    print(GREEN + str(grid[i][j]) + RESET, end=", ")
                elif max(hehe, key=hehe.get) == 2:
                    print(RED + str(grid[i][j]) + RESET, end=", ")
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
        return (True,min(a,b)) if (math.gcd(a,b) in [a,b] and a != 0 and b != 0) else (False,0)
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
    
    def extractPrimesFrom(self, n, i):
        stack = [(n, i)]
        min_value = n
        while stack:
            current_n, idx = stack.pop()
            if idx >= len(self.seeds):
                if current_n < min_value:
                    min_value = current_n
                continue
            seed = self.seeds[idx]
            if seed <= 1:
                stack.append((current_n, idx + 1))
                continue
            stack.append((current_n, idx + 1))
            temp = current_n
            while (temp % seed == 0 and temp > 1):
                temp //= seed
                stack.append((temp, idx + 1))

        return min_value
    def fixSeeds(self):
        new_seeds = []
        add_score = 0
        for seed in self.seeds:
            for i in range(4):
                for j in range(4):
                    if self.grid[i][j] != 0 and self.grid[i][j] % seed == 0:
                        new_seeds.append(seed)
            if seed not in new_seeds:
                add_score += seed
        return list(set(new_seeds)), add_score


        
    def extractNewPrimes(self, n):
        n = self.extractPrimesFrom(n, 0)
        if n > 0:
            return [n]
        return []
    def merge_grid(self, grid):
        changed = False
        add_score = 0
        newprimes = []

        for i in range(4):
            for j in range(3):  # no out-of-bounds
                a = grid[i][j]
                b = grid[i][j+1]

                can_merge, score = DIVE.merges(a, b)
                if can_merge:
                    add_score += score
                    newprimes += self.extractNewPrimes(a + b)

                    grid[i][j] = a + b
                    grid[i][j+1] = 0
                    changed = True

        return grid, changed, add_score, newprimes
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
    def get_tile_merges(grid, X,Y):
        tile = grid[Y][X]
        mergers = 0

        gaze = (Y-1,X)
        while gaze[0] >= 0 and grid[gaze[0]][gaze[1]] == 0:
            gaze = (gaze[0]-1, gaze[1])
        if gaze[0] >= 0 and DIVE.merges(tile, grid[gaze[0]][gaze[1]])[0]:
            mergers+=1

        gaze = (Y+1,X)
        while gaze[0] <= 3 and grid[gaze[0]][gaze[1]] == 0:
            gaze = (gaze[0]+1, gaze[1])
        if gaze[0] <= 3 and DIVE.merges(tile, grid[gaze[0]][gaze[1]])[0]:
            mergers+=1

        
        gaze = (Y,X-1)
        while gaze[1] >= 0 and grid[gaze[0]][gaze[1]] == 0:
            gaze = (gaze[0], gaze[1]-1)
        if gaze[1] >= 0 and DIVE.merges(tile, grid[gaze[0]][gaze[1]])[0]:
            mergers+=1

        gaze = (Y,X+1)
        while gaze[1] <= 3 and grid[gaze[0]][gaze[1]] == 0:
            gaze = (gaze[0], gaze[1]+1)
        if gaze[1] <= 3 and DIVE.merges(tile, grid[gaze[0]][gaze[1]])[0]:
            mergers+=1
        return mergers
    def get_num_merges(self):
        mergers = 0
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] != 0:
                    mergers += DIVE.get_tile_merges(self.grid, i,j)
        return mergers
    def move_left(self):
        self.grid, changed1 = DIVE.compress_grid(self.grid)
        self.grid, changed2, new_score, newPrimes = self.merge_grid(self.grid)
        changed = changed1 or changed2
        self.grid = DIVE.compress_grid(self.grid)[0]
        return self.grid, changed, new_score, newPrimes
    
    def move_right(self):
        self.grid = DIVE.reverse_grid(self.grid)
        self.grid, changed, score, primes = self.move_left()
        self.grid = DIVE.reverse_grid(self.grid)
        return self.grid, changed, score, primes

    def move_up(self):
        self.grid = DIVE.transpose_grid(self.grid)
        self.grid, changed, score, primes = self.move_left()
        self.grid = DIVE.transpose_grid(self.grid)
        return self.grid, changed, score, primes

    def move_down(self):
        self.grid = DIVE.transpose_grid(self.grid)
        self.grid = DIVE.reverse_grid(self.grid)
        self.grid, changed, score, primes = self.move_left()
        self.grid = DIVE.reverse_grid(self.grid)
        self.grid = DIVE.transpose_grid(self.grid)
        return self.grid, changed, score, primes
    def move(self, move="l"):
        func = {
            "l": self.move_left,
            "r": self.move_right,
            "u": self.move_up,
            "d": self.move_down
        }[move]
        new_grid, changed, score, newprimes = func()
        if changed:
            self.grid = new_grid
            self.changed = changed
            self.score += score
            self.seeds += newprimes
            self.seeds = [seed for seed in self.seeds if seed != 1]
            self.seeds, add_score = self.fixSeeds()
            self.score += add_score
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
    def get_zeros_next_to_tile(grid, X,Y):
        adjacents = [(Y,X)]
        for i in range(10):
            for j in adjacents:
                new_adj = []
                if j[0] > 0 and (j[0]-1,j[1]) not in adjacents and grid[j[0]-1][j[1]] == 0:
                    new_adj.append((j[0]-1,j[1]))
                if j[1] > 0 and (j[0],j[1]-1) not in adjacents and grid[j[0]][j[1]-1] == 0:
                    new_adj.append((j[0],j[1]-1))
                if j[0] < 3 and (j[0]+1,j[1]) not in adjacents and grid[j[0]+1][j[1]] == 0:
                    new_adj.append((j[0]+1,j[1]))
                if j[1] < 3 and (j[0],j[1]+1) not in adjacents and grid[j[0]][j[1]+1] == 0:
                    new_adj.append((j[0],j[1]+1))
            adjacents += new_adj
        adjacents.remove((Y,X))
        return adjacents
    def add_new_tile(grid, new_tile=2):
        try:
            position = random.choice(DIVE.get_zeros(grid))
            grid[position[0]][position[1]] = new_tile
        except IndexError:
            pass
        return grid
    def reset_grid(self):
        self.grid = DIVE.add_new_tile(DIVE.add_new_tile([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]))
        return self
    def NEW():
        return DIVE(seeds=[2]).reset_grid()
    
    
    def get_largest_tile(self):
        lt = 0
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] > lt:
                    lt = self.grid[i][ j]
        return lt
    def get_pos_largest_tile(self):
        lt = 0
        lt_pos = (0,0)
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] > lt:
                    lt = self.grid[i][j]
                    lt_pos = (i,j)
        return lt_pos
    def prepare(self):
        self.fixSeeds()
        DIVE.add_new_tile(self.grid, random.choice(self.seeds))
        return self
    def user_play(self, wasd_mode=True):
        while len(DIVE.get_zeros(self.grid)) > 0:
            if not wasd_mode:
                while (x:=input()) not in ["l","r","u","d"]:
                    pass
                self.move(x)
            else:
                while (x:=input()) not in ["w","a","s","d"]:
                    pass
                self.move({"w":"u","a":"l","s":"d","d":"r"}[x])
            self.prepare()
            self.self_pp()

'''-=- testing zone ^w^ -=-'''
if __name__ == "__main__":
    arr = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ]
    A = DIVE(grid=arr, name="DIVE", seeds=[2])
    A.reset_grid()
    A.self_pp()
    A.user_play()
