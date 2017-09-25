import LinRegLearner,BagLearner 
class InsaneLearner(object): # six lines, wow!
    def __init__(self, verbose=False): self.bl = BagLearner.BagLearner(BagLearner.BagLearner,kwargs={'learner': LinRegLearner.LinRegLearner,'bags': 20}, bags = 20)
    def author(self): return 'hsikka3'
    def addEvidence(self, Xtrain, Ytrain): self.bl.addEvidence(Xtrain,Ytrain)
    def query(self, Xtest): self.bl.query(Xtest)

