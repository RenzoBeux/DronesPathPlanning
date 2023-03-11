import matplotlib.pyplot as plt

BATCH_SIZE=37

def average(arr:list[float]):
  total = 0
  for num in arr:
    total += num
  return total/len(arr)


readFile = open('./salida.txt','r')
lines = readFile.readlines()
readFile.close()
evals:list[float] = []
evalsGraph:list[float] = []
evalEntropys:list[float] = []
evalEntropysGraph:list[float] = []
regularEntropys:list[float] = []
regularEntropysGraph:list[float] = []
combinedEntropys:list[float] = []
combinedEntropysGraph:list[float] = []
betas:list[float] = []
betasGraph:list[float] = []
alfas:list[float] = []
alfasGraph:list[float] = []
epoch:int = 0

for line in lines:
  if line[0] != 'T':
    words = line.split(' ')
    evals.append(float(words[1]))
    evalEntropys.append(float(words[4]))
    regularEntropys.append(float(words[7]))
    combinedEntropys.append(float(words[10]))
    betas.append(float(words[-1]))
    alfas.append(float(words[-3]))
  else:
    evalsGraph.append(average(evals))
    evalEntropysGraph.append(average(evalEntropys))
    regularEntropysGraph.append(average(regularEntropys))
    combinedEntropysGraph.append(average(combinedEntropys))
    alfasGraph.append(average(alfas))
    betasGraph.append(average(betas))
    evals = []
    evalEntropys = []
    regularEntropys = []
    combinedEntropys = []
    betas = []
    alfas = []
    epoch += 1
    
xAxis = [x for x in range(epoch)]

# Solid
# Dashed
# Dotted
# Dashdot

plt.plot(xAxis,evalsGraph,label='eval',linestyle='solid')
# plt.plot(xAxis,evalEntropysGraph,label='evalEntropy')
plt.plot(xAxis,regularEntropysGraph,label='regularEntropy',linestyle='dashed')
plt.plot(xAxis,combinedEntropysGraph,label='combinedEntropy',linestyle='dotted')
plt.plot(xAxis,alfasGraph,label='alfa',linestyle='dashdot')
# plt.plot(xAxis,betasGraph,label='beta',linestyle='solid')
# plt.ylim(-0.3,8)
plt.legend()
plt.show()

#     file = open('./salida.txt','r')
# lines = file.readlines()
# file.close()
# file = open('./graph.txt','w')
# for i,line in enumerate(lines):
#   words = line.split(' ')
#   eval = words[1]
#   evalEntropy = words[4]
#   regularEntropy = words[7]
#   combinedEntropy = words[10]
#   beta = float(words[-1])
#   alfa = float(words[-3])
#   file.write("{} {} {} {} {} {} {}\n".format(i,eval,evalEntropy,regularEntropy,combinedEntropy,alfa,beta))
