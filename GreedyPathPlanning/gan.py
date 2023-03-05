# -*- coding: utf-8 -*-
"""CleanTesisAlmeidaBeux.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18f357af9hjIS-cGyOwWpf6QYcT8cjo78

## Imports
"""

from tensorflow.keras import layers, optimizers
from collections import Counter
import tensorflow as tf
from enum import Enum
import numpy as np 
import time
import os

tf.config.run_functions_eagerly(True)

print(tf.__version__)

"""### Classes

#### coordObject
"""

class coordObject:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def copy(self):
      return coordObject(self.x,self.y)

"""#### Obstacle"""

class Obstacle:

    def __init__(self, dimsInit: coordObject, dimsEnd: coordObject, id: int):
        self.dimsInit = dimsInit
        self.dimsEnd = dimsEnd
        self.id = id

    def toSections(self, gridDimensions: coordObject):
        sections = []
        percentageOfSectionInitX = gridDimensions.x * self.dimsInit.x
        percentageOfSectionEndX = gridDimensions.x * self.dimsEnd.x
        percentageOfSectionInitY = gridDimensions.y * self.dimsInit.y
        percentageOfSectionEndY = gridDimensions.y * self.dimsEnd.y
        sectionInitX = int(percentageOfSectionInitX)
        sectionEndX = int(percentageOfSectionEndX)
        sectionInitY = int(percentageOfSectionInitY)
        sectionEndY = int(percentageOfSectionEndY)
        for i in range(sectionInitX, sectionEndX+1):
            for j in range(sectionInitY, sectionEndY+1):
                sections.append(coordObject(i, j))
        return sections

"""#### POI"""

class POI:
    def __init__(self, coords: coordObject, expectedVisitTime: int, id: int):
        # coords is (x,y) pair of numbers in [0..1]
        self.coords = coords
        if (self.coords.x == 1):
            self.coords.x = 0.99
        if (self.coords.y == 1):
            self.coords.y = 0.99
        self.expectedVisitTime = expectedVisitTime
        self.lastVisit = 0
        self.id = id

    def getSection(self, dim: coordObject) -> coordObject:
        percentageOfSectionX = dim.x * self.coords.x
        percentageOfSectionY = dim.y * self.coords.y
        sectionX = int(percentageOfSectionX)
        sectionY = int(percentageOfSectionY)
        result = coordObject(sectionX, sectionY)
        return result

    def markVisited(self, time):
        self.lastVisit = time

"""### Constants"""

###########
# CONTEXT #
###########
DIM = coordObject(15, 15)
BIGDIM = coordObject(30, 30)
ORIGIN = coordObject(0, 0)
UAVAMOUNT = 6
TIMELENGTH = 200
POIS = [coordObject(0.031, 0.909), coordObject(0.56, 0.09),
        coordObject(0.937, 0.09), coordObject(0.937, 0.909)]
POIS_TIMES = [10, 18, 18, 18]
OBSTACLES = [
    Obstacle(coordObject(0.32, 0.45), coordObject(0.7, 0.54), 0),
    Obstacle(coordObject(0.94, 0.4), coordObject(0.95, 0.5), 1),
]

OBS_PUNISH = 0.9
# Time to charge must be aprox 2.5 times the BATTERY_CAPACITY
BATTERY_CAPACITY = 40
TIME_TO_CHARGE = 90

###############
# GAN RELATED #
###############
EPOCHS = 512
BUFFER_SIZE = 1131
BATCH_SIZE = 32
NOISE_DIM = 200

GEN_LEARNING_RATE=0.0001
DISC_LEARNING_RATE=0.00001

EVAL_LOSS_WEIGHT=1
REGULAR_LOSS_WEIGHT=0

num_examples_to_generate = 3
seed = tf.random.normal([num_examples_to_generate, NOISE_DIM])
#########
# OTHER #
#########
class ACTION(Enum):
    STAY = 0
    RIGHT = 1
    DIAG_DOWN_RIGHT = 2
    DOWN = 3
    DIAG_DOWN_LEFT = 4
    LEFT = 5
    DIAG_UP_LEFT = 6
    UP = 7
    DIAG_UP_RIGHT = 8


colors = ['b', 'g', 'r', 'c', 'm', 'k']
markers = ['o', '^', 'v', '<', '>', 's',
           'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']

metrics = ['Coverage', 'Collision', 'Obstacles', 'POIS', 'Uptime']

"""## Datastet preparation"""

#!unzip -qq output.zip

def parseFile(fileName):
  file = open(fileName, 'r')
  res = []
  for line in file:
    res.append(list(map(lambda x: int(x), line.split())))
  return np.array(res)

def load_real_samples():
  trainX = []
  trainy = []
  for dir in os.listdir('./output'):
    for fileName in os.listdir('./output/'+dir):
      trainX.append(parseFile('./output/'+dir+'/'+fileName))
      trainy.append(1)
  trainX = np.array(trainX)
  trainy = np.array(trainy)
  X = trainX.astype('float32')
  X = (X - 4) / 4
  return X

train_images = load_real_samples()
train_images = train_images.reshape(-1, UAVAMOUNT, TIMELENGTH, 1)
train_dataset = tf.data.Dataset.from_tensor_slices(train_images)

"""## Custom Evaluator

### Helpers
"""

# given a list of lists of ints, returns a list of ACTIONS
def parseMoves(listOfLists):
    res = []
    for line in listOfLists:
        res.append(list(map(lambda x: ACTION(x), line)))
    return res

# this will return a matrix of lists of ints where each int is the time a drone passed by that square
def populateArea(actions, areaDims: coordObject):
    # res will have areadims.x * areadims.y elements
    res: list[list[list[int]]] = []
    timeOOB = 0
    # initialize res with 0s
    for i in range(areaDims.x):
        res.append([])
        for j in range(areaDims.y):
            res[i].append([])
    # here we will store current pos for each drone
    currentPos: list[coordObject] = []
    # for each drone we will initialize its current point in 0,0
    for i in range(UAVAMOUNT):
        currentPos.append(ORIGIN.copy())
    # we mark the initial point of each drone as visited
    for i in range(UAVAMOUNT):
      res[currentPos[i].x][currentPos[i].y].append(0)
    # for each drone
    for i in range(UAVAMOUNT):
        # we will iterate through the actions
        for j in range(TIMELENGTH):
            chosenMove = actions[i][j]
            if chosenMove == ACTION.RIGHT:
                currentPos[i].x = currentPos[i].x + 1
            elif chosenMove == ACTION.DIAG_DOWN_RIGHT:
                currentPos[i].x = currentPos[i].x + 1
                currentPos[i].y = currentPos[i].y - 1
            elif chosenMove == ACTION.DOWN:
                currentPos[i].y = currentPos[i].y - 1
            elif chosenMove == ACTION.DIAG_DOWN_LEFT:
                currentPos[i].y = currentPos[i].y - 1
                currentPos[i].x = currentPos[i].x - 1
            elif chosenMove == ACTION.LEFT:
                currentPos[i].x = currentPos[i].x - 1
            elif chosenMove == ACTION.DIAG_UP_LEFT:
                currentPos[i].x = currentPos[i].x - 1
                currentPos[i].y = currentPos[i].y + 1
            elif chosenMove == ACTION.UP:
                currentPos[i].y = currentPos[i].y + 1
            elif chosenMove == ACTION.DIAG_UP_RIGHT:
                currentPos[i].y = currentPos[i].y + 1
                currentPos[i].x = currentPos[i].x + 1
            outOfBounds =not (currentPos[i].x in range(areaDims.x) and currentPos[i].y in range(areaDims.y))
            if(outOfBounds):
                timeOOB += 1
            else:
                res[currentPos[i].x][currentPos[i].y].append(j)
    return res, timeOOB

def get_duplicates(array):
    c = Counter(array)
    return {k: v for k, v in c.items() if v > 1}

"""### Quality Evaluation Functions

##### Collission
"""

# This function will reward if drones don't share the same square at the same time
def evaluateDronesCollision(actions, areaDims: coordObject, area) -> float:
    worstCase = UAVAMOUNT * TIMELENGTH 
    res = 0
    for i in range(areaDims.x):
        for j in range(areaDims.y):
            # find the repeted times in the list
            # we dont want to take into account the base
            if (i == ORIGIN.x and j == ORIGIN.y):
                continue
            duplicates = get_duplicates(area[i][j])
            for k in duplicates:
                res = res + duplicates[k]

    return 1 - (res / worstCase)

"""##### Coverage"""

# This function evaluates the coverage of the area
def evaluateCoverageArea(actions, areaDims: coordObject, area) -> float:
    numberOfSquares = areaDims.x * areaDims.y
    res = numberOfSquares
    for i in range(areaDims.x):
        for j in range(areaDims.y):
            if len(area[i][j]) == 0:
                res = res - 1
    return res / numberOfSquares

"""##### Obstacles"""

def flatten_obstacles(areaDims:coordObject):
    """
    Returns a list of all of the coordinates which are considered occupied by obstacles
    """
    obstaclesBySections:list[list[coordObject]] = list(map(lambda obs:obs.toSections(areaDims),OBSTACLES))
    flat_obs:list[coordObject] = []
    # Suboptimal as all hell
    for sectionList in obstaclesBySections:
        for section in sectionList:
            isAccounted = False
            for alreadyAccounted in flat_obs:
                if(alreadyAccounted.x == section.x and alreadyAccounted.y == section.y):
                    isAccounted = True
                    break
            if(not isAccounted):
                flat_obs.append(section)
    return flat_obs

# This function will reward drones for not flying over obstacles
def evaluateObstacles(actions, areaDims: coordObject, area) -> float:
    # Worst case is considered as every drone spending every instant over an obstacle
    worstCase = UAVAMOUNT * TIMELENGTH
    flat_obs = flatten_obstacles(areaDims)
    timeOnObs = 0
    for obs in flat_obs:
      timeOnObs += len(area[obs.x][obs.y])
    return 1 - timeOnObs / worstCase

"""##### POI Visit"""

def evaluatePOICoverage(actions, areaDims: coordObject, area) -> float:
    timeSpentNeedy = [0 for _ in POIS]
    lastVisit = [0 for _ in POIS]
    time = TIMELENGTH
    # list of objects is needed to access aux functions
    pois = [POI(coords, 0, 0) for coords in POIS]

    for t in range(time):
        for i, poi in enumerate(pois):
            coords = poi.getSection(areaDims)
            if(t in area[coords.x][coords.y]):
                lastVisit[i] = t
            elif(t - lastVisit[i] > POIS_TIMES[i]):
                timeSpentNeedy[i] += 1

    totalTimeSpentNeedy = 0
    for needy in timeSpentNeedy:
        totalTimeSpentNeedy += needy

    maxNeedyTimes = [time-poiTime for poiTime in POIS_TIMES]
    maximumNeediness = 0
    for needy in maxNeedyTimes:
        maximumNeediness += needy

    return 1 - totalTimeSpentNeedy/maximumNeediness

"""##### UAV Uptime"""

# This function will return the best score if at all times there is at least one UAV outside base
def evaluateDroneUpTime(actions, areaDims: coordObject, area) -> float:
    dronesUp = 0
    breaked = False
    for t in range(TIMELENGTH):
        for i in range(areaDims.x):
            if breaked:
                breaked = False
                break
            for j in range(areaDims.y):
                # we dont want to take into account the base
                if (i == ORIGIN.x and j == ORIGIN.y):
                    continue
                if(t in area[i][j]):
                    dronesUp += 1
                    breaked = True
                    break
    return dronesUp/TIMELENGTH

"""### Evaluator"""

def evaluate(grid):
  # Lets check all drone routes are valid
  area,timeOOB = populateArea(grid,DIM)
  # Further evaluators must be added to this dictionary
  evaluators = {'Coverage':evaluateCoverageArea,'Collision':evaluateDronesCollision,'Obstacles':evaluateObstacles,'POIS':evaluatePOICoverage, 'Uptime': evaluateDroneUpTime}
  evaluateMetric = lambda eval: eval(grid,DIM,area)
  results = {metric:evaluateMetric(eval) for metric, eval in evaluators.items()}
  # Out of bound is elevated so as to exascervate errors in this field
  results['OutOfBound'] = (1 - timeOOB / (UAVAMOUNT * TIMELENGTH)) ** 2
  # print(results['OutOfBound'])
  return results['OutOfBound']
  accumulator = 0
  for v in results.values():
      accumulator += v
  return accumulator/len(results)

def evaluateGAN(generatedList):
    """
    Returns the average of all of the metrics for a given set of moves
    """
    parsedList = parseMoves(generatedList)
    results = evaluate(parsedList)
    return results

"""## Model Generation

### Generator
"""

def make_generator_model():
    n_nodes = 128 * 2 * 50
    model = tf.keras.Sequential()

    model.add(layers.Dense(n_nodes, input_shape=(NOISE_DIM,)))

    model.add(layers.LeakyReLU(alpha=0.2))

    model.add(layers.Reshape((2, 50, 128)))

    model.add(layers.Conv2DTranspose(128, (6,4), strides=(3,2), padding='same'))
    model.add(layers.LeakyReLU(alpha=0.2))
    
    model.add(layers.Conv2DTranspose(128, (1,4),  strides=(1,2), padding='same'))
    model.add(layers.LeakyReLU(alpha=0.2))

    model.add(layers.Conv2D(1, (2,50), activation='tanh', padding='same'))

    return model
generator = make_generator_model()
generator.summary()

"""#### Loss"""

def generator_loss(fake_output):
    cross_entropy = tf.keras.losses.BinaryCrossentropy()
    return cross_entropy(tf.ones_like(fake_output), fake_output)

def evaluatorOutputLoss(evaluations,fake_output, evalWeight, regularWeight):
    cross_entropy = tf.keras.losses.BinaryCrossentropy()
    ev = cross_entropy(tf.ones_like(evaluations),evaluations)
    reg = cross_entropy(tf.ones_like(fake_output), fake_output)
    res = evalWeight * ev +  regularWeight * reg
    # print(ev.numpy())
    print("Eval: " + str(np.mean(evaluations)) +" | EvCrossEntropy: " + str(ev.numpy()) + " | RegCrossEntropy: " + str(reg.numpy()) + " | CombCrossEntropy: " + str(res.numpy()) + " | alfa,beta: " + str(evalWeight) + " , " + str(regularWeight) ) 
    return res

"""#### Optimizer"""

generator_optimizer = tf.keras.optimizers.Adam(learning_rate=GEN_LEARNING_RATE)

"""### Discriminator"""

def make_discriminator_model():
    model = tf.keras.Sequential()

    #downsample
    model.add(layers.Conv2D(128, (3,3), strides=(2,2), padding='same', input_shape=(UAVAMOUNT,TIMELENGTH,1))) #3x100x128
    model.add(layers.LeakyReLU(alpha=0.2))

    #downsample
    model.add(layers.Conv2D(128, (3,3), strides=(2,2), padding='same', input_shape=(3,100,1))) #2x50x128
    model.add(layers.LeakyReLU(alpha=0.2))
    
    # classifier
    model.add(layers.Flatten())
    model.add(layers.Dropout(0.4))
    model.add(layers.Dense(1, activation='sigmoid'))

    # opt = optimizers.Adam(lr=0.0002, beta_1=0.5)
    # model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])

    return model
discriminator = make_discriminator_model()
discriminator.summary()

"""#### Loss"""

def discriminator_loss(real_output, fake_output):
    cross_entropy = tf.keras.losses.BinaryCrossentropy()
    real_loss = cross_entropy(tf.ones_like(real_output), real_output)
    fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
    total_loss = real_loss + fake_loss
    return total_loss

"""#### Optimizer"""

discriminator_optimizer = tf.keras.optimizers.Adam(learning_rate=DISC_LEARNING_RATE)

"""## Training

### Train Step
"""

# This annotation causes the function to be "compiled".
@tf.function
def train_step(images,epoch,epochs):
    noise = tf.random.normal([BATCH_SIZE, NOISE_DIM])
    evaluations = tf.TensorArray(dtype=tf.float32, size=0, dynamic_size=True)
    fake_img = generator(noise, training=False)
    with tf.GradientTape() as disc_tape:
      real_output = discriminator(images, training=True)
      fake_output = discriminator(fake_img, training=True)
      disc_loss = discriminator_loss(real_output, fake_output)

    gradients_of_discriminator = disc_tape.gradient(disc_loss, discriminator.trainable_variables)
    discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, discriminator.trainable_variables))

    with tf.GradientTape() as gen_tape:
      gen_imgs = generator(noise, training=True)
      for x,route in enumerate(gen_imgs):
        evaluation = evaluateGAN((route.numpy().reshape(UAVAMOUNT,TIMELENGTH) * 4 + 4).round())
        evaluations = evaluations.write(x,evaluation)
      evaluations = evaluations.stack()
      predicted = discriminator(gen_imgs, training=False)
      # gen_loss = generator_loss(predicted)
      gen_loss = evaluatorOutputLoss(evaluations,predicted, epoch/epochs, (epochs - epoch)/epochs )
    
    gradients_of_generator = gen_tape.gradient(gen_loss, generator.trainable_variables)
    generator_optimizer.apply_gradients(zip(gradients_of_generator, generator.trainable_variables))

    return (gen_loss, disc_loss)

"""### Model Training"""

def generate_and_save_images(model, epoch, test_input):
  predictions = model(test_input, training=False)

  for i in range(predictions.shape[0]):
    with open('Generated'+str(i)+'.txt', 'w') as writefile:
      for line in predictions[i, :, :, 0]:
        writefile.write(' '.join([str(int(x)) for x in (line.numpy() * 4 + 4).round()]) + '\n')

def train(dataset, epochs):
  for epoch in range(epochs):
    avgGenLoss = 0
    avgDisLoss = 0
    batched = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE)
    start = time.time()

    for image_batch in batched:
      gLoss, dLoss = train_step(image_batch,epoch,epochs-1)
      avgGenLoss += gLoss / BATCH_SIZE
      avgDisLoss += dLoss / BATCH_SIZE

    print ('Time for epoch {} is {} sec // gLoss: {} | dLoss: {}'.format(epoch + 1, time.time()-start, avgGenLoss, avgDisLoss))

  # Generate after the final epoch
  generate_and_save_images(generator,epochs,seed)

"""# RUN"""

train(train_dataset, EPOCHS)