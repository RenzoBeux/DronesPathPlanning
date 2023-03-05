from os import listdir
from torch import float32, ones as torchOnes, tensor, zeros as torchZeros, randn,Tensor
from torch.utils.data import DataLoader, TensorDataset

from constants import constants

def label_real(size:int):
  return torchOnes(size,1).to(constants.device)

def label_fake(size:int):
  return torchZeros(size,1).to(constants.device)

def create_noise(size:int,nz:int):
  return randn(size,nz)

def load_dataset():
  input_files = listdir('./input')
  all_file_routes:list[int] = []
  for i in input_files:
    file = open(f"./input/{i}",'r')
    file_lines = file.readlines()
    file.close()
    file_routes = list(map(lambda x : list(map(float, x.split(' '))),file_lines))
    all_file_routes.append(file_routes)
  files_tensor_routes = tensor(all_file_routes,dtype=float32) / 4 - 1
  _labels = torchZeros(len(files_tensor_routes))
  files_dataset = TensorDataset(files_tensor_routes,_labels)
  route_loader = DataLoader(files_dataset,batch_size=constants.BATCH_SIZE,shuffle=True)
  tensor_shape = files_tensor_routes.shape
  return route_loader, tensor_shape

def output_to_moves(route:Tensor):
  return ((route + 1) * 4).round()

def tensor_to_file(tensor_routes:Tensor,file_name:str):
  route_samples:list[list[float]] = tensor_routes.tolist()
  for (i,sample) in enumerate(route_samples):
    file = open(f"{file_name}.{i}.txt",'w')
    for route in sample:
      for move in route:
        file.write(f"{str(int(move))} ")
      file.write('\n')
    file.close()
