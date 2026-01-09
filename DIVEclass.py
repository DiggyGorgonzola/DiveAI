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

    def get_prime_factors(n):
        facts = {5:0,3:0,2:0}
        for i in [5, 3, 2]:
            while n % i == 0 and n != 0:
                n //= i
                facts[i]+=1
        return facts
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
            for j in range(0,3):
                if DIVE.merges(grid[i][j], grid[i][j+1])[0]:
                    add_score += DIVE.merges(grid[i][j], grid[i][j+1])[1]

                    newprimes += self.extractNewPrimes(grid[i][j]+grid[i][j+1])
                    grid[i][j] = grid[i][j] + grid[i][j+1]
                    grid[i][j+1] = 0
                    changed = True
        print(newprimes)
        newprimes = sorted(list(set(newprimes)))
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
    
    def move_left(self):
        new_grid, changed1 = DIVE.compress_grid(self.grid)
        new_grid, changed2, new_score, newPrimes = self.merge_grid(new_grid)
        changed = changed1 or changed2
        new_grid = DIVE.compress_grid(new_grid)[0]
        return new_grid, changed, new_score, newPrimes
    
    def move_right(self):
        self.grid = DIVE.reverse_grid(self.grid)
        new_grid, changed, score, primes = self.move_left()
        new_grid = DIVE.reverse_grid(new_grid)
        return new_grid, changed, score, primes

    def move_up(self):
        self.grid = DIVE.transpose_grid(self.grid)
        new_grid, changed, score, primes = self.move_left()
        new_grid = DIVE.transpose_grid(new_grid)
        return new_grid, changed, score, primes

    def move_down(self):
        self.grid = DIVE.transpose_grid(self.grid)
        self.grid = DIVE.reverse_grid(self.grid)
        new_grid, changed, score, primes = self.move_left()
        new_grid = DIVE.reverse_grid(new_grid)
        new_grid = DIVE.transpose_grid(new_grid)
        return new_grid, changed, score, primes
    def move(self, move="l"):
        func = {
            "l": self.move_left,
            "r": self.move_right,
            "u": self.move_up,
            "d": self.move_down
        }[move]

        new_grid, changed, score, newprimes = func()
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
    def add_new_tile(grid, new_tile=2):
        position = random.choice(DIVE.get_zeros(grid))
        grid[position[0]][position[1]] = new_tile
        return grid
    def reset_grid(self):
        self.grid = DIVE.add_new_tile(DIVE.add_new_tile([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]))
        return self
    
    
    def get_largest_tile(self):
        lt = 0
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] > lt:
                    lt = self.grid[i][j]
        return lt
    def user_play(self, wasd_mode=True):
        while len(DIVE.get_zeros(self.grid)) > 0:
            if not wasd_mode:
                while (x:=input()) not in ["l","r","u","d"]:
                    pass
                self.move(x)
                DIVE.add_new_tile(self.grid, random.choice(self.seeds))
                self.self_pp()
            else:
                while (x:=input()) not in ["w","a","s","d"]:
                    pass
                self.move({"w":"u","a":"l","s":"d","d":"r"}[x])
                DIVE.add_new_tile(self.grid, random.choice(self.seeds))
                self.self_pp()

'''-=- testing zone ^w^ -=-'''
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
