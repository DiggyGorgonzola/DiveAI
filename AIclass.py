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
    DIVELL, DIVELR, DIVELU, DIVELD, DIVERL, DIVERR, DIVERU, DIVERD, DIVEUL, DIVEUR, DIVEUU, DIVEUD, DIVEDL, DIVEDR, DIVEDU, DIVEDD = (DIVE(grid=self.dive.grid, score=self.dive.score, seeds=self.dive.seeds, changed=self.dive.changed),)*16
    a = {"ll":AI.score_position(DIVELL.move("l").move("l"), self.weights),
         "lr":AI.score_position(DIVELR.move("l").move("r"), self.weights),
         "lu":AI.score_position(DIVELU.move("l").move("u"), self.weights),
         "ld":AI.score_position(DIVELD.move("l").move("d"), self.weights),

         "rl":AI.score_position(DIVERL.move("r").move("l"), self.weights),
         "rr":AI.score_position(DIVERR.move("r").move("r"), self.weights),
         "ru":AI.score_position(DIVERU.move("r").move("u"), self.weights),
         "rd":AI.score_position(DIVERD.move("r").move("d"), self.weights),

         "ul":AI.score_position(DIVEUL.move("u").move("l"), self.weights),
         "ur":AI.score_position(DIVEUR.move("u").move("r"), self.weights),
         "uu":AI.score_position(DIVEUU.move("u").move("u"), self.weights),
         "ud":AI.score_position(DIVEUD.move("u").move("d"), self.weights),

         "dl":AI.score_position(DIVEDL.move("d").move("l"), self.weights),
         "dr":AI.score_position(DIVEDR.move("d").move("r"), self.weights),
         "du":AI.score_position(DIVEDU.move("d").move("u"), self.weights),
         "dd":AI.score_position(DIVEDD.move("d").move("d"), self.weights)}
        #Get the best move
    self.dive = self.dive.move(AI.get_key(a, a[max(a, key=a.get)])[0])
    self.dive.grid = DIVE.add_new_tile(self.dive.grid, random.choice(self.dive.seeds))
    self.dive = self.dive.move(AI.get_key(a, a[max(a, key=a.get)])[1])
    self.dive.grid = DIVE.add_new_tile(self.dive.grid, random.choice(self.dive.seeds))
    return self.dive
  def give_birth(self, juvenoia=1):
    child_weights = self.weights
    for i in range(len(self.weights)):
      child_weights[i] += juvenoia*(random.random()-1/2)
      
    return AI(weights=child_weights, name=self.name+f".child{round(1000*random.random(),3)}", parent=self, dive=DIVE.NEW())
  def run_till_death(self):
    while len(DIVE.get_zeros(self.dive.grid)) > 0:
      self.step()
    return self

class TheTormenter():
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
      self.g_next.append(winner.give_birth(i))
    self.g_first = self.g_next
    self.g_next = []
    self.g_first_scores = {}
    return winner
  
  def TORTURE(self, base, target):
    winner = base
    while base.dive.score < target:
      try:
        base.dive = DIVE.NEW()
        print(TT.TORMENT())
        winner = TT.POPULATE()
        print("WINNER:",winner.name,"\nWEIGHTS:",winner.weights, "\nSCORE:",winner.dive.score)
        base = winner
      except:
        pass
    return winner


'''-=- testing zone -=- :3'''

guh = AI([76.87868355314122, 24.2506177131773, -148.91126384565317, 63.32513101152392, -7.648193259774409], parent=None, dive=DIVE.NEW())
TT = TheTormenter([guh, guh.give_birth(), guh.give_birth(), guh.give_birth(), guh.give_birth(), guh.give_birth(), guh.give_birth()])
while True:
  TT.TORTURE(guh,1000)
