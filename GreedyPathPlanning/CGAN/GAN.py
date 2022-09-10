from GreedyPathPlanning.CGAN.discriminator import Discriminator
from GreedyPathPlanning.CGAN.generator import Generator
from keras.models import Sequential
from keras.optimizers import Adam
from utils import readFileAction
from evaluator import evaluate

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

class CGAN():
    def __init__(self):
        self.discriminator = Sequential()
        self.discriminator.compile(loss=['binary_crossentropy'],optimizer=Adam(0.0002, 0.5),metrics=['acurracy'])
        self.generator = Generator()
        pass