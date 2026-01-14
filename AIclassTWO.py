import math, random, time
from DIVEclass import DIVE

class AI():
    def __init__(self, dive=None, mode="MAX0"):
        self.dive = dive or DIVE.NEW()
        self.mode = mode
        randy = lambda:2*random.random()-1
    def score_position(dive, weights):
        score = 0
        FUNCS = [len(DIVE.get_zeros(dive.grid)), max(dive.seeds), len(dive.seeds), dive.score, dive.get_num_merges(), len(DIVE.get_zeros_next_to_tile(dive.grid, dive.get_pos_largest_tile()[1],dive.get_pos_largest_tile()[0]))]
        for i in range(len(FUNCS)):
            score += (weights[i])*(FUNCS[i])
        return score
    def futures(self):
        futures_dict = {}
        for name, func in {
                "l": self.dive.move_left,
                "r": self.dive.move_right,
                "u": self.dive.move_up,
                "d": self.dive.move_down,
            }.items():
            g,c,s,ns=func()
            glork = DIVE(grid=g, changed=c, score=self.dive.score+s,seeds=self.dive.seeds+ns, name=self.dive.name+f".{name}")
            glork.fixSeeds()
            futures_dict[name]=glork
        return futures_dict
    def futures2(self):
        mwah = self.futures()
        for key,Diver in mwah.items():
            mwah[key] = AI(dive=Diver).futures()
        return mwah
    def get_best_move(self,mode="MAX0"):
        best_move, best_move_score = [random.choice(list("lrud")),random.choice(list("lrud"))],0
        if mode == "MAX0":
            weights=[100,-100,-999,50,-10,200]
            posiblemoves = self.futures2()
            for i in ["l", "r", "u", "d"]:
                for j in ["l", "r", "u", "d"]:
                    if s:=AI.score_position(posiblemoves[i][j],weights) > best_move_score:
                        best_move, best_move_score = [i,j],s
            return (best_move, best_move_score)
        elif mode == "TARG":
            weights=[200,-999,-300,0,-10,400]
            posiblemoves = self.futures2()
            for i in ["l", "r", "u", "d"]:
                for j in ["l", "r", "u", "d"]:
                    if s:=AI.score_position(posiblemoves[i][j],weights) > best_move_score:
                        best_move, best_move_score = [i,j],s
            return (best_move, best_move_score)
        elif mode == "SEED":
            weights=[200,999,-500,100,-10,400]
            posiblemoves = self.futures2()
            for i in ["l", "r", "u", "d"]:
                for j in ["l", "r", "u", "d"]:
                    if s:=AI.score_position(posiblemoves[i][j],weights) > best_move_score:
                        best_move, best_move_score = [i,j],s
            return (best_move, best_move_score)
        elif mode == "SUCI":
            weights=[999,0,-100,0,999,500]
            posiblemoves = self.futures2()
            for i in ["l", "r", "u", "d"]:
                for j in ["l", "r", "u", "d"]:
                    if s:=AI.score_position(posiblemoves[i][j],weights) > best_move_score:
                        best_move, best_move_score = [i,j],s
            return (best_move, best_move_score)
        return (best_move, best_move_score)
    def change_mode(self):
        if self.dive.score < 300:
            self.mode = "MAX0"
        elif max(self.dive.seeds) > len(self.dive.seeds)+1:
            self.mode = "TARG"
        elif len(DIVE.get_zeros(self.dive.grid)) < 5:
            self.mode = "SUCI"
        elif self.dive.score > 300 and len(DIVE.get_zeros(self.dive.grid)) > 12:
            self.mode = "SEED"
        else:
            self.mode = "RAND"
    def step2(self,dbg=False):
        for i in self.get_best_move(self.mode)[0]:
            if dbg:
                print("Moved",i)
                print(f"Mode: {self.mode}")
            self.dive.move(i)
            self.dive.fixSeeds()
            DIVE.add_new_tile(self.dive.grid, random.choice(self.dive.seeds))
            if dbg:
                self.dive.self_pp()
            self.change_mode()
    def run(self, times):
        total_score=0
        top_score=0 
        for _ in range(times):
            self.dive = DIVE.NEW().reset_grid()
            while self.dive.get_num_merges() > 0 or len(DIVE.get_zeros(self.dive.grid)) > 0:
                self.step2()
            total_score += self.dive.score
            if top_score < self.dive.score:
                top_score = self.dive.score
            print(f"{round(_/times*100,math.ceil(math.log10(times)))}% done", flush=True)
        print("TOP SCORE:", top_score)
        print("AVG SCORE:", total_score/times)

"""INVOLVE THE MODES SYSTEM!!!"""


'''nuclear test site :3'''

'''FUNCS = [len(DIVE.get_zeros(dive.grid)), max(dive.seeds), len(dive.seeds), dive.score, dive.get_num_merges(), len(DIVE.get_zeros_next_to_tile(dive.grid, dive.get_pos_largest_tile()[1],dive.get_pos_largest_tile()[0]))]
'''
ai = AI()
ai.run(200)
