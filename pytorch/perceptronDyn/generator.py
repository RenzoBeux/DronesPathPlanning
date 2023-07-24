from torch.nn import Module, Linear, Sequential, Tanh, LeakyReLU
from torch.nn.modules.loss import _Loss
from torch.optim import Optimizer
from constants import constants
import math
import numpy as np
from utils import label_real
from discriminator import Discriminator
from approaches import WeightApproach
from CustomLoss import CustomLoss


class Generator(Module):
    def __init__(self, noise_dim):
        super(Generator, self).__init__()
        self.noise_dim = noise_dim
        self.main = Sequential(
            Linear(self.noise_dim, 256),
            LeakyReLU(0.2),
            Linear(256, 512),
            LeakyReLU(0.2),
            Linear(512, 1024),
            LeakyReLU(0.2),
            Linear(1024, constants.uav_amount * constants.time_lenght),
            Tanh(),
        )

    def forward(self, x):
        return self.main(x).view(-1, constants.uav_amount, constants.time_lenght)


def train_generator(
    discriminator: Discriminator, g_optimizer: Optimizer, data_fake, eval_tensor, epoch
):
    curr_batch_size = data_fake.size(0)
    real_label = label_real(curr_batch_size)
    g_optimizer.zero_grad()
    output = discriminator(data_fake)

    evalWeight, regularWeight = WeightApproach.get_instance().get_weights(epoch)

    print(f"evalWeight: {evalWeight}, regularWeight: {regularWeight}")

    loss_fun = CustomLoss(eval_tensor, evalWeight, regularWeight)
    loss = loss_fun(output, real_label)
    loss.backward()
    g_optimizer.step()
    return loss
