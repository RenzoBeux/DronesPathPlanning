import matplotlib.pyplot as plt

def graph_output(file_name:str):
  file = open(file_name,'r')
  lines = file.readlines()
  file.close()
  graph = {x.replace(':',''):[] for x in lines[0].split(' ')[::2]}
  for line in lines:
    line_split = list(map(lambda x : x.replace(':',''),line.split(' ')))
    keys = line_split[::2]
    values = list(map(lambda x: float(x.replace('\n','')),line_split[1::2]))
    for i,key in enumerate(keys):
      vals = graph[key]
      vals.append(values[i])
      graph[key] = vals
  for key,val in graph.items():
    if key == "Epoch" or key == "time":
      continue
    plt.plot(val,label=key)
  plt.legend()
  plt.show()


import argparse
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--input", help="File to interpret", dest="input", type=str)
  args = parser.parse_args()
  graph_output(args.input)