from os import makedirs
from os.path import isdir
from time import time
from torch import FloatTensor, save, load
from torch.nn import BCELoss
from torch.optim import Adam

from constants import constants
from evaluator import evaluateGAN, evaluator_loss
from discriminator import Discriminator, train_discriminator
from generator import Generator, train_generator
from utils import create_noise, load_dataset, output_to_moves, tensor_to_file

from CustomLoss import CustomLoss


def save_checkpoint(model, optimizer, epoch, filename):
    checkpoint = {
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }
    save(checkpoint, filename)


def load_checkpoint(model, optimizer, filename):
    checkpoint = load(filename)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    epoch = checkpoint['epoch']

    return model, optimizer, epoch


print(f"Working on {constants.device}")
route_loader, tensor_shape = load_dataset()

print(f"dataset_size {tensor_shape[0]}")
print(f"uav_amount: {tensor_shape[1]}")
print(f"time_length: {tensor_shape[2]}")


# Instantiate the generator and discriminator networks
generator = Generator(constants.NOISE_DIM).to(constants.device)
discriminator = Discriminator().to(constants.device)

# Define the loss function and optimizer for the discriminator
d_loss_fun = BCELoss()

g_optim = Adam(generator.parameters(), lr=constants.g_learn_rate)
d_optim = Adam(discriminator.parameters(), lr=constants.d_learn_rate)

noise = create_noise(constants.sample_size, constants.NOISE_DIM)

evals: list[float] = []
e_losses: list[float] = []
images = []
# Define the training loop
for epoch in range(constants.EPOCHS):
    start = time()
    g_loss = 0.0
    d_loss = 0.0
    epoch_g_loss = 0.0
    epoch_d_loss = 0.0
    for i, (images, _) in enumerate(route_loader):
        images = images.to(constants.device)
        curr_batch_size = images.size(0)

        for step in range(constants.K):  # Optional if we always consider k as 1
            data_fake = generator(create_noise(
                curr_batch_size, constants.NOISE_DIM))
            data_real = images
            d_loss += train_discriminator(discriminator,
                                          d_loss_fun, d_optim, data_real, data_fake)

        data_fake = generator(create_noise(
            curr_batch_size, constants.NOISE_DIM))

        move_list = output_to_moves(data_fake).tolist()
        evaluations = list(map(evaluateGAN, move_list))
        eval_tensor = FloatTensor(evaluations).to(constants.device)
        eval_avg = eval_tensor.mean()
        evals.append(eval_avg)

        g_loss += train_generator(discriminator,
                                  g_optim, data_fake, eval_tensor)
        eval_tensor.detach()
        del eval_tensor
        epoch_g_loss = float(g_loss) / (i+1)
        epoch_d_loss = float(d_loss) / (i+1)
    end = time()
    if epoch % 20 == 0:
        if not isdir('output'):
            makedirs('output')
        generated_img = generator(noise).cpu().detach()
        move_tensor = output_to_moves(generated_img)
        tensor_to_file(move_tensor, f'output/test.{epoch}')

    print(
        f"Epoch: {epoch} time: {end-start} eval: {eval_avg} combined_loss: {epoch_g_loss} d_loss: {epoch_d_loss}")
generated_img = generator(noise).cpu().detach()
move_tensor = output_to_moves(generated_img)
tensor_to_file(move_tensor, f'output/test.{constants.EPOCHS}')
