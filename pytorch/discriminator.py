from torch import Tensor
from torch.nn import Module, Linear, Sequential, LeakyReLU, Dropout, Sigmoid
from torch.nn.modules.loss import _Loss
from torch.optim import Optimizer

from utils import label_fake, label_real
from constants import constants

class Discriminator(Module):
  def __init__(self):
    super(Discriminator, self).__init__()
    self.n_input = constants.uav_amount * constants.time_lenght
    self.main = Sequential(
      Linear(self.n_input, 1024),
      LeakyReLU(0.2),
      Dropout(0.3),
      Linear(1024, 512),
      LeakyReLU(0.2),
      Dropout(0.3),
      Linear(512, 256),
      LeakyReLU(0.2),
      Dropout(0.3),
      Linear(256, 1),
      Sigmoid(),
    )

  def forward(self, x):
    x = x.view(-1, self.n_input)
    return self.main(x)

def train_discriminator(discriminator:Discriminator,loss_fun:_Loss, d_optimizer:Optimizer, 
                        data_real:Tensor, data_fake:Tensor):
  curr_batch_size = data_real.size(0)
  real_label = label_real(curr_batch_size)
  fake_label = label_fake(curr_batch_size)
  d_optimizer.zero_grad()
  output_real = discriminator(data_real)
  loss_real = loss_fun(output_real, real_label)
  output_fake = discriminator(data_fake)
  loss_fake = loss_fun(output_fake, fake_label)
  loss_real.backward()
  loss_fake.backward()
  d_optimizer.step()
  return loss_real + loss_fake
