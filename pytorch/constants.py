from os import listdir
from torch import device,cuda, tensor



class Constants_Class(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(Constants_Class, cls).__new__(cls)
    return cls.instance

  def __init__(self):
    self.set_uav_amount_and_time()
    self.set_device()

  def set_uav_amount_and_time(self):
    input_files = listdir('./input')
    single_file = listdir(f"./input/{input_files[0]}")
    file = open(f"./input/{input_files[0]}/{single_file[0]}",'r')
    file_lines = file.readlines()
    file.close()
    file_routes = list(map(lambda x : [list(map(int, x.split(' ')))],file_lines))
    files_tensor_routes = tensor(file_routes,dtype=int)
    self.uav_amount = files_tensor_routes.shape[0]
    self.time_lenght =files_tensor_routes.shape[2]

  def set_device(self):
    self.device= device('cuda' if cuda.is_available() else 'cpu')

  BATCH_SIZE = 512
  EPOCHS = 256
  sample_size = 3 # fixed sample size
  NOISE_DIM = 128 # latent vector size
  K = 1 # number of steps to apply to the discriminator
  device
  uav_amount:int = None
  time_lenght:int = None
   
constants = Constants_Class()










