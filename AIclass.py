import DIVE, random

class AI():
  def __init__(self, weights=[], name="AI", parent=None, dive=None):
    self.weights = weights
    self.name = name
    self.parent = parent
    self.dive = dive
  def score_position(dive):
    score = 0
    FUNCS = [len(DIVE.get_zeros(dive)), max(dive.seeds), len(dive.seeds), dive.score, dive.score+DIVE.move_left(dive.grid),dive.score+DIVE.move_right(dive.grid),dive.score+DIVE.move_up(dive.grid),dive.score+DIVE.move_down(dive.grid)]
    for i in self.weights:
      score += i*FUNCS
    return score
  def step(self):
    a = {"l":DIVE(grid=DIVE.move_left(self.dive.grid)),
         "r":DIVE(DIVE.move_right(self.dive.grid)),
         "u":DIVE(DIVE.move_up(self.dive.grid)),
         "d":DIVE(DIVE.move_down(self.dive.grid))
        #Get the best move
    b = a
    for i in list(a.keys():
      b[i] = AI.score_position(b[i])
    self.dive = b[max(a, keys=a.get)]
    return self.dive
  def give_birth(self, juvenoia=1):
    child_weights = self.weights
    for i in self.weights:
      child_weights += juvenoia*(random.random()-1/2)
      
    return AI(weights=child_weights, name=self.name+".child", parent=self, dive=DIVE(seeds=[2]).reset_grid())
'''-=- testing zone -=- :3'''

guh = AI([0,0,0,0], parent=self, dive=DIVE(seeds=[2]).reset_grid())
