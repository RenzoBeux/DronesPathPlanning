from os import makedirs
from os.path import isdir, exists
from time import time
from torch import FloatTensor, manual_seed
from torch.nn import BCELoss
from torch.optim import Adam


from constants import constants
from evaluator import evaluateGAN
from discriminator import Discriminator, train_discriminator
from generator import Generator, train_generator
from utils import create_noise, load_dataset, output_to_moves, tensor_to_file
from torch import save

from evaluator import EvaluatorModules

from approaches import EvaluatorModuleApproach

from CustomLoss import CustomLoss

manual_seed(42)
print(f"Working on {constants.device}")
route_loader, tensor_shape = load_dataset()

print(f"dataset_size {tensor_shape[0]}")
print(f"uav_amount: {tensor_shape[1]}")
print(f"time_length: {tensor_shape[2]}")

# Print the constants
print(f"NOISE_DIM: {constants.NOISE_DIM}")
print(f"sample_size: {constants.sample_size}")
print(f"K: {constants.K}")
print(f"EPOCHS: {constants.EPOCHS}")
print(f"g_learn_rate: {constants.g_learn_rate}")
print(f"d_learn_rate: {constants.d_learn_rate}")
print(f"Weight Approach: {constants.weightApproach}")
print(f"Evaluator Approach: {constants.evaluatorModuleApproach}")

# Instantiate the generator and discriminator networks
generator = Generator(constants.NOISE_DIM).to(constants.device)
discriminator = Discriminator().to(constants.device)

# Define the loss function and optimizer for the discriminator
d_loss_fun = BCELoss()

g_optim = Adam(generator.parameters(), lr=constants.g_learn_rate)
d_optim = Adam(discriminator.parameters(), lr=constants.d_learn_rate)

noise = create_noise(constants.sample_size, constants.NOISE_DIM)

g_losses: list[float] = []
d_losses: list[float] = []
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
            data_fake = generator(create_noise(curr_batch_size, constants.NOISE_DIM))
            data_real = images
            d_loss += train_discriminator(
                discriminator, d_loss_fun, d_optim, data_real, data_fake
            )

        data_fake = generator(create_noise(curr_batch_size, constants.NOISE_DIM))

        move_list = output_to_moves(data_fake).tolist()
        evaluatorModules = EvaluatorModuleApproach.get_instance().get_evaluator_modules(
            epoch
        )
        evaluations = list(
            map(lambda x: evaluateGAN(x, evaluatorModules), move_list)
        )
        eval_tensor = FloatTensor(evaluations).to(constants.device)

        eval_avg = eval_tensor.mean()

        g_loss += train_generator(discriminator, g_optim, data_fake, eval_tensor, epoch)

        eval_tensor.detach()
        del eval_tensor

        epoch_g_loss = float(g_loss) / (i + 1)
        epoch_d_loss = float(d_loss) / (i + 1)
    end = time()
    if epoch % 20 == 0:
        if not isdir("output"):
            makedirs("output")
        generated_img = generator(noise).cpu().detach()
        move_tensor = output_to_moves(generated_img)
        tensor_to_file(move_tensor, f"output/test.{epoch}")

    print(
        f"Epoch: {epoch} time: {end-start} eval: {eval_avg} combined_loss: {epoch_g_loss} d_loss: {epoch_d_loss}"
    )
generated_img = generator(noise).cpu().detach()
move_tensor = output_to_moves(generated_img)
tensor_to_file(move_tensor, f"output/test.{constants.EPOCHS}")

# Save the models
save(generator.state_dict(), "output/generator_model.pth")
save(discriminator.state_dict(), "output/discriminator_model.pth")
