from utils import readFileAction
from evaluator import evaluate
from tensorflow import keras

def parseInputs():
    x_train = []
    y_train = []
    for probToTarget in range(70,100):
        for i in range(1,10):
            fileName = './output/'+str(probToTarget)+'/'+str(i)+'.txt'
            setOfRoutes = readFileAction(fileName)
            scores = evaluate(setOfRoutes)
            score = 0
            for v in scores.values():
                score += v
            score /= len(scores)
            x_train.append(setOfRoutes)
            y_train.append(score) 

class CGAN(keras.Model):
    def __init__(self,discriminator,generator):
        super(CGAN,self).__init__()
        self.discriminator = discriminator
        self.generator = generator

    def compile(self,d_optimizer,g_optimizer,loss_fn):
        super(CGAN,self).compile()
        self.d_optimizer = d_optimizer
        self.g_optimizer = g_optimizer
        self.loss_fn = loss_fn
    