from torch.nn import Module, Linear, Sequential, Tanh, LeakyReLU
from torch.nn.modules.loss import _Loss
from torch.optim import Optimizer
from constants import constants

from utils import label_real
from discriminator import Discriminator

class Generator(Module):
  def __init__(self,noise_dim):
    super(Generator, self).__init__()
    self.noise_dim = noise_dim
    self.main = Sequential(
      Linear(self.noise_dim,256),
      LeakyReLU(0.2),
      Linear(256,512),
      LeakyReLU(0.2),
      Linear(512,1024),
      LeakyReLU(0.2),
      Linear(1024,constants.uav_amount * constants.time_lenght),
      Tanh(),
    )

  def forward(self, x):
    return self.main(x).view(-1, constants.uav_amount, constants.time_lenght)

def train_generator(discriminator:Discriminator,loss_fun:_Loss,g_optimizer:Optimizer, data_fake):
  curr_batch_size = data_fake.size(0)
  real_label = label_real(curr_batch_size)
  g_optimizer.zero_grad()
  output = discriminator(data_fake)
  loss = loss_fun(output, real_label)
  loss.backward()
  g_optimizer.step()
  return loss