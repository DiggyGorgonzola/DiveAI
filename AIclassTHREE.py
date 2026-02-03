from DIVEclass import DIVE
import random, math, time
def createDive():
    return DIVE(seeds=[2]).reset_grid()

def value(dive):
    r = .5*(random.random() - 1/2)
    a = dive.listify().count(0) ** 2 / 10
    b = len(dive.seeds)
    c = math.log(max(dive.seeds))
    d = math.log(dive.score + .001) / 100

    G = dive.get_pos_largest_tile()
    e = len(DIVE.get_zeros_next_to_tile(dive.grid, G[1], G[0]))
    return a - b + c

def get_best_move(dive):
    a={}
    for i in range(4):
        for j in range(4):
            for k in range(4):
                x = dive.copy()
                a["lrud"[i]+"lrud"[j]+"lrud"[k]] = value(x.move("lrud"[i]).move("lrud"[j]).move("lrud"[k]))
    return max([(value, key) for key, value in a.items()])[1][0]
def run(db=False):
    a = createDive()
    while a.listify().count(0) > 0 or a.get_num_merges() > 0 and not len(a.seeds) > 10:
        if random.random() < .99:
            a.move(get_best_move(a))
        else:
            a.move(random.choice("lrud"))
        a.prepare()
        if db:
            a.self_pp()
            time.sleep(.5)
    return a.score


for i in range(10):
    print(run())
