from DIVEclass import DIVE
import random

class AI():
  def __init__(self, weights=[], name="AI", parent=None, dive=None):
    self.weights = weights
    self.name = name
    self.parent = parent
    self.dive = dive
  def score_position(dive):
    score = 0
    FUNCS = [len(DIVE.get_zeros(dive.grid)), max(dive.seeds), len(dive.seeds), dive.score, dive.score+DIVE.move_left(dive.grid),dive.score+DIVE.move_right(dive.grid),dive.score+DIVE.move_up(dive.grid),dive.score+DIVE.move_down(dive.grid)]
    for i in dive.weights:
      score += i*FUNCS
    return score
  def step(self):
    DL = self.dive.move_left()
    DR = self.dive.move_right()
    DU = self.dive.move_up()
    DD = self.dive.move_down()

    a = {"l":DIVE(grid=DL[0],changed=DL[1],score=(self.dive.score+DL[2]), seeds=(self.dive.seeds+DL[3])),
         "r":DIVE(grid=DR[0],changed=DR[1],score=(self.dive.score+DR[2]), seeds=(self.dive.seeds+DR[3])),
         "u":DIVE(grid=DU[0],changed=DU[1],score=(self.dive.score+DU[2]), seeds=(self.dive.seeds+DU[3])),
         "d":DIVE(grid=DD[0],changed=DD[1],score=(self.dive.score+DD[2]), seeds=(self.dive.seeds+DD[3]))}
        #Get the best move
    b = [0,0,0,0]
    for i in list(a.keys()):
      a[i].self_pp()
    for i in range(4):
      b[i] = AI.score_position(a[list(a.keys())[i]])
    self.dive = b[max(a, keys=a.get)]
    return self.dive
  def give_birth(self, juvenoia=1):
    child_weights = self.weights
    for i in self.weights:
      child_weights += juvenoia*(random.random()-1/2)
      
    return AI(weights=child_weights, name=self.name+".child", parent=self, dive=DIVE(seeds=[2]).reset_grid())
'''-=- testing zone -=- :3'''

guh = AI([0,0,0,0], parent=None, dive=DIVE(seeds=[2]).reset_grid())
guh.step()
guh.dive.self_pp()
