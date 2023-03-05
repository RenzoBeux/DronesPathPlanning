from torch.nn import BCELoss
from torch.optim import Adam

from constants import constants
from discriminator import Discriminator, train_discriminator
from generator import Generator, train_generator
from utils import create_noise,load_dataset,output_to_moves,tensor_to_file

print(f"Working on {constants.device}")

route_loader,tensor_shape = load_dataset()

print(f"dataset_size {tensor_shape[0]}")
print(f"uav_amount: {tensor_shape[1]}")
print(f"time_length: {tensor_shape[2]}")

# Instantiate the generator and discriminator networks
generator = Generator(constants.NOISE_DIM).to(constants.device)
discriminator = Discriminator().to(constants.device)

# Define the loss function and optimizer for the discriminator
d_loss_fun = BCELoss()
g_loss_fun = BCELoss()
g_optim = Adam(generator.parameters(), lr=0.0002)
d_optim = Adam(discriminator.parameters(), lr=0.0002)

noise = create_noise(constants.sample_size,constants.NOISE_DIM)

g_losses:list[float] = []
d_losses:list[float] = []
images = []
# Define the training loop
for epoch in range(constants.EPOCHS):
  g_loss = 0.0
  d_loss = 0.0
  epoch_g_loss = 0.0
  epoch_d_loss = 0.0
  for i, (images,_) in enumerate(route_loader):
    images = images.to(constants.device)
    curr_batch_size = images.size(0)

    for step in range(constants.K): # Optional if we always consider k as 1
      data_fake = generator(create_noise(curr_batch_size,constants.NOISE_DIM)).detach()
      data_real = images
      d_loss += train_discriminator(discriminator,d_loss_fun,d_optim,data_real,data_fake)

    data_fake = generator(create_noise(curr_batch_size,constants.NOISE_DIM))
    g_loss += train_generator(discriminator,g_loss_fun,g_optim,data_fake)

    if i % 20 == 0:
      generated_img = generator(noise).cpu().detach()
      move_tensor = output_to_moves(generated_img)
      tensor_to_file(move_tensor,f'output/test.{i}')

    epoch_g_loss = g_loss / i
    epoch_d_loss = d_loss / i
    g_losses.append(epoch_g_loss)
    d_losses.append(epoch_d_loss)
  print(f"Epoch:{epoch} g_loss:{epoch_g_loss} d_loss:{epoch_d_loss}")