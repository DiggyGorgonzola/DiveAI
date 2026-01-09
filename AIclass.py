from DIVEclass import DIVE
import random, time

class AI():
  def __init__(self, weights=[], name="AI", parent=None, dive=None):
    self.weights = weights
    self.name = name
    self.parent = parent
    self.dive = dive
  def score_position(dive, weights):
    score = 0
    FUNCS = [len(DIVE.get_zeros(dive.grid)), max(dive.seeds), len(dive.seeds), dive.score, dive.get_num_merges()]
    for i in range(len(weights)):
      score += (weights[i])*(FUNCS[i])
    return score
  def get_key(d, val):
    for key, value in d.items():
      if value == val:
        return key
    return None
  def step(self):
    DIVEL, DIVER, DIVEU, DIVED = DIVE(grid=self.dive.grid, score=self.dive.score, seeds=self.dive.seeds, changed=self.dive.changed),DIVE(grid=self.dive.grid, score=self.dive.score, seeds=self.dive.seeds, changed=self.dive.changed),DIVE(grid=self.dive.grid, score=self.dive.score, seeds=self.dive.seeds, changed=self.dive.changed),DIVE(grid=self.dive.grid, score=self.dive.score, seeds=self.dive.seeds, changed=self.dive.changed)
    a = {"l":AI.score_position(DIVEL.move("l"), self.weights),
         "r":AI.score_position(DIVER.move("r"), self.weights),
         "u":AI.score_position(DIVEU.move("u"), self.weights),
         "d":AI.score_position(DIVED.move("d"), self.weights)}
        #Get the best move
    self.dive = self.dive.move(AI.get_key(a, a[max(a, key=a.get)]))
    self.dive.grid = DIVE.add_new_tile(self.dive.grid, random.choice(self.dive.seeds))
    return self.dive
  def give_birth(self, juvenoia=1):
    child_weights = self.weights
    for i in range(len(self.weights)):
      child_weights[i] += juvenoia*(random.random()-1/2)
      
    return AI(weights=child_weights, name=self.name+f".child{round(random.random(),3)}", parent=self, dive=DIVE.NEW())
  def run_till_death(self):
    while len(DIVE.get_zeros(self.dive.grid)) > 0:
      self.step()
    return self

class The_Tormenter():
  g_first = []
  g_first_scores = {}
  g_next = []
  def __init__(self,g_first=[]):
    self.g_first=g_first
  def TORMENT(self):
    for i in self.g_first:
      i.run_till_death()
      self.g_first_scores[i] = i.dive.score
    return self.g_first_scores
  def POPULATE(self):
    winner = AI.get_key(self.g_first_scores,self.g_first_scores[max(self.g_first_scores,key=self.g_first_scores.get)])
    self.g_next.append(winner)
    for i in range(len(self.g_first)-1):
      self.g_next.append(winner.give_birth())
    self.g_first = self.g_next
    self.g_next = []
    self.g_first_scores = {}
    return winner

'''-=- testing zone -=- :3'''

guh = AI([100,50,-50,10,20], parent=None, dive=DIVE.NEW())
TT = The_Tormenter([guh, guh.give_birth(), guh.give_birth(), guh.give_birth(), guh.give_birth(), guh.give_birth(), guh.give_birth()])
print(TT.TORMENT())
winner = TT.POPULATE()
print("WINNER:",winner.name,"\nWEIGHTS:",winner.weights)
