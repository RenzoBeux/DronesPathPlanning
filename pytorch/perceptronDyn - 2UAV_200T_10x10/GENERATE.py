from utils import create_noise
from constants import constants
import torch
from generator import Generator
from utils import create_noise, output_to_moves, tensor_to_file



# load the generator
generator = Generator(constants.NOISE_DIM).to(constants.device)
generator.load_state_dict(torch.load('generator_model.pth'))

# Make sure we are in evaluation mode
generator.eval()

# Create random noise vectors
noise = create_noise(constants.sample_size, constants.NOISE_DIM)

# Generate images
with torch.no_grad():
    generated_images = generator(noise).cpu().detach()

# At this point `generated_images` is a tensor with your generated images (or movements in your case)

# Save the generated images in txt file named GENERATOR.txt
move_tensor = output_to_moves(generated_images)
tensor_to_file(move_tensor, f'GENERATED.txt')