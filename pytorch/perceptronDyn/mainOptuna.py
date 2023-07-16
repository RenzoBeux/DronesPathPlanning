import optuna

from os import makedirs
from os.path import isdir, exists
from time import time
from torch import FloatTensor
from torch.nn import BCELoss
from torch.optim import Adam
from torch import save

from constants import constants
from evaluator import evaluateGAN, evaluator_loss
from discriminator import Discriminator, train_discriminator
from generator import Generator, train_generator
from utils import create_noise, load_dataset, output_to_moves, tensor_to_file

from CustomLoss import CustomLoss

def objective(trial):
    # Define the hyperparameters to optimize
    g_learn_rate = trial.suggest_loguniform('g_learn_rate', 1e-4, 1e-1)
    d_learn_rate = trial.suggest_loguniform('d_learn_rate', 1e-4, 1e-1)
    noise_dim = trial.suggest_int('noise_dim', 10, 128)
    # Set the constants with the optimized hyperparameters
    constants.g_learn_rate = g_learn_rate
    constants.d_learn_rate = d_learn_rate
    constants.NOISE_DIM = noise_dim

    print(f"Trial: {trial.number}")
    print(f"g_learn_rate: {g_learn_rate}")
    print(f"d_learn_rate: {d_learn_rate}")
    print(f"noise_dim: {noise_dim}")

    # Train the model with the new hyperparameters
    generator = Generator(constants.NOISE_DIM).to(constants.device)
    discriminator = Discriminator().to(constants.device)

    d_loss_fun = BCELoss()

    g_optim = Adam(generator.parameters(), lr=constants.g_learn_rate)
    d_optim = Adam(discriminator.parameters(), lr=constants.d_learn_rate)

    noise = create_noise(constants.sample_size, constants.NOISE_DIM)


    g_losses: list[float] = []
    d_losses: list[float] = []
    evals: list[float] = []
    e_losses: list[float] = []
    images = []
    eval_avg = 0

    for epoch in range(constants.EPOCHS):
        start = time()
        g_loss = 0.0
        d_loss = 0.0
        epoch_g_loss = 0.0
        epoch_d_loss = 0.0
        for i, (images, _) in enumerate(route_loader):
            images = images.to(constants.device)
            curr_batch_size = images.size(0)

            for step in range(constants.K):
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

            g_loss += train_generator(discriminator,
                                      g_optim, data_fake, eval_tensor, epoch)

            eval_tensor.detach()
            del eval_tensor

            epoch_g_loss = float(g_loss) / (i+1)
            epoch_d_loss = float(d_loss) / (i+1)
        end = time()
        if epoch % 20 == 0:
            if not isdir(f'output/{trial.number}'):
                makedirs(f'output/{trial.number}')
            generated_img = generator(noise).cpu().detach()
            move_tensor = output_to_moves(generated_img)
            tensor_to_file(move_tensor, f'output/{trial.number}/test.{epoch}')

        print(
            f"Epoch: {epoch} time: {end-start} eval: {eval_avg} combined_loss: {epoch_g_loss} d_loss: {epoch_d_loss}")
    generated_img = generator(noise).cpu().detach()
    move_tensor = output_to_moves(generated_img)
    tensor_to_file(move_tensor, f'output/{trial.number}/test.{constants.EPOCHS}')

    # Save the models
    # save(generator.state_dict(), 'generator_model.pth')
    # save(discriminator.state_dict(), 'discriminator_model.pth')

    # Return the evaluation metric to optimize
    return eval_avg

if not isdir('output'):
    makedirs('output')

route_loader, tensor_shape = load_dataset()

print(f"dataset_size {tensor_shape[0]}")
print(f"uav_amount: {tensor_shape[1]}")
print(f"time_length: {tensor_shape[2]}")

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=15)

# Print the best hyperparameters and evaluation metric
print('Best trial:')
trial = study.best_trial
print('  Value: {}'.format(trial.value))
print('  Params: ')
for key, value in trial.params.items():
    print('    {}: {}'.format(key, value))