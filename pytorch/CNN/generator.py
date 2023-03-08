from torch.nn import Module, Linear, Sequential, Tanh, LeakyReLU .
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
           Linear(latent_size, 64 * (output_size // 8)),
           ReLU(),
           ConvTranspose1d(64, 32, kernel_size=5, stride=2, padding=2),
           ReLU(),
           ConvTranspose1d(32, 16, kernel_size=5, stride=2, padding=2),
           ReLU(),
           ConvTranspose1d(16, 1, kernel_size=5, stride=2, padding=2),
           Tanh()
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