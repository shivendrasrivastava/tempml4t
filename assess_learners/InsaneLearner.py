import LinRegLearner,BagLearner 
class InsaneLearner(object):
    def __init__(self, verbose=False): pass
    def author(self): return 'hsikka3'
    def addEvidence(self, Xtrain, Ytrain): 
      self.bl = BagLearner.BagLearner(BagLearner.BagLearner,kwargs={'learner': LinRegLearner.LinRegLearner,'bags': 20}, bags = 20)
      self.bl.addEvidence(Xtrain,Ytrain)
    def query(self, Xtest): self.bl.query(Xtest)

