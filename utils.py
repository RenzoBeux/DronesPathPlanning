import numpy as np
import matplotlib.pyplot as plt

file = open('./input.txt','r')
routes = file.readlines()
file.close()
splitroutes = list(map(lambda x: x.split(' '),routes))
epochEval = []
epochEvalCrossEntropy = []
epochRegularEntropy = []
epochCombinedEntropy = []
epochAlfa = []
epochBeta = []

meanEpochEval = []
meanEpochEvalCrossEntropy = []
meanEpochRegularEntropy = []
meanEpochCombinedEntropy = []
meanEpochAlfa = []
meanEpochBeta = []

for route in splitroutes:
  if(route[0] == 'Time'):
    meanEpochEval.append(np.array(epochEval).mean())
    meanEpochEvalCrossEntropy.append(np.array(epochEvalCrossEntropy).mean())
    meanEpochRegularEntropy.append(np.array(epochRegularEntropy).mean())
    meanEpochCombinedEntropy.append(np.array(epochCombinedEntropy).mean())
    meanEpochAlfa.append(np.array(epochAlfa).mean())
    meanEpochBeta.append(np.array(epochBeta).mean())
    
    epochEval = []
    epochEvalCrossEntropy = []
    epochRegularEntropy = []
    epochCombinedEntropy = []
    epochAlfa = []
    epochBeta = []
  else:
    epochEval.append(float(route[1]))
    epochEvalCrossEntropy.append(float(route[4]))
    epochRegularEntropy.append(float(route[7]))
    epochCombinedEntropy.append(float(route[10]))
    epochAlfa.append(float(route[-1]))
    epochBeta.append(float(route[-3]))


plt.plot(meanEpochEval)
plt.show()