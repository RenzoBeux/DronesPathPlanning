# from tensorflow import keras
# from keras import models, layers, Input
from GreedyPathPlanning.utils import readFileAction
from GreedyPathPlanning.evaluator import evaluate
# from GreedyPathPlanning.utils import readFileAction
# from GreedyPathPlanning.evaluator import evaluate

# import tensorflow as tf
# import numpy as np



x_train = []
y_train = []
for probToTarget in range(70,100):
    for i in range(1,10):
        fileName = './GreedyPathPlanning/output/'+str(probToTarget)+'/'+str(i)+'.txt'
        setOfRoutes = readFileAction(fileName)
        scores = evaluate(setOfRoutes)
        score = 0
        for v in scores.values():
            score += v
        score /= len(scores)
        x_train.append(setOfRoutes)
        y_train.append(score)
print(y_train)



# model = models.Sequential()
# model.add(Input(shape=(1)))
# model.add(layers.Dense(1,activation='relu'))
# model.add(layers.Dense(1))

# print(model.output_shape)

# model.compile(loss='categorical_crossentropy',optimizer='adam')
# model.fit([[1],[1],[1],[1],[1]],[1,1,1,1,1])