import os

def moveToOHE(move:str):
  """
  Returns the one hot encoding of a move
  """
  res = ['0','0','0','0','0','0','0','0']
  if(move == '0'):
    return res
  intMove = int(move) - 1
  res[intMove] = '1'
  return res

def oheEncoder():
  """
  Creates another output directory with the paths listed in one hot encoding manner
  """
  for dir in os.listdir('./output'):
    for fileName in os.listdir('./output/'+dir):
      file = open('./output/'+dir+'/'+fileName,'r')
      routes = file.readlines()
      file.close()
      movesInMoves:list[list[str]] = list(map(lambda x: x.split(' '),routes))
      movesInOHE:list[list[list[str]]] = list(map(lambda x: list(map(lambda y:moveToOHE(y),x)),movesInMoves))
      if not os.path.exists('OHEOutput'):
        os.makedirs('OHEOutput')
      if not os.path.exists('OHEOutput/'+dir):
        os.makedirs('OHEOutput/'+dir)
      output = open('./OHEOutput/'+dir+'/'+fileName,"a")
      for uavRoute in movesInOHE:
        route = str.join(' ',list(map(lambda move:str.join(' ',move),uavRoute)))
        output.write(route)
        output.write('\n')
      output.close()


def OHEToMove(move:list[str]):
  """
  This function is to be called with a list of 8 characters, of which at most one is a 1
  """
  try:
    return move.index('1') + 1
  except:
    return 0
  

def fromOHE(lines:list[str]):
  """
  Pass to this function the output from the readlines function on the open file
  """
  for line in lines:
    newLine = line.replace('\n','')
    oheMoves = newLine.split(' ')
    for i in range(0,len(oheMoves),8):
      print(oheMoves[i:i+8])


oheEncoder()