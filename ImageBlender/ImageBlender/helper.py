# CONVOLUTION FUNCTION

# === IMPORTS ===
import numpy as np
import matplotlib.pyplot as plt
from skimage import data, color, img_as_float, io
import os
from PIL import Image
from scipy.ndimage import gaussian_filter1d

# === DEFINE PADDING ===
def add_padding(image, pad_height, pad_width, mode):
  if mode == 'clip':
      return image  # no padding, "valid" convolution region only
  elif mode == 'zero':
      return np.pad(image, ((pad_height, pad_height), (pad_width, pad_width), (0, 0)), mode='constant')
  elif mode == 'wrap':
       return np.pad(image, ((pad_height, pad_height), (pad_width, pad_width), (0, 0)), mode='wrap')
  elif mode == 'copy':
      return np.pad(image, ((pad_height, pad_height), (pad_width, pad_width), (0, 0)), mode='edge')
  elif mode == 'reflect':
      return np.pad(image, ((pad_height, pad_height), (pad_width, pad_width), (0, 0)), mode='reflect')
  else:
      raise ValueError("Padding mode must be one of ['clip', 'zero', 'wrap', 'copy', 'reflect'].")

# === DEFINE COVOLUTION FUNCTION ===
def conv2(input_image, kernel, pad_mode):
  # Flip kernel (for convolution, not correlation
  kernel = np.flipud(np.fliplr(kernel))

  # Handle grayscale by adding a channel dimension
  if input_image.ndim == 2:
      input_image = input_image[..., np.newaxis]

  height, width, channels = input_image.shape
  kernel_height, kernel_width = kernel.shape
  pad_height, pad_width = kernel_height // 2, kernel_width // 2

  # Apply padding
  padded_image = add_padding(input_image, pad_height, pad_width, pad_mode)

  # Output shape
  if pad_mode == 'clip':
      output_height = height - 2 * pad_height
      output_width = width - 2 * pad_width
  else:
      output_height, output_width = height, width

  # Initialize output
  img_conv = np.zeros((output_height, output_width, channels))

  # Perform convolution channel-wise
  for c in range(channels):
      for i in range(output_height):
          for j in range(output_width):
              region = padded_image[i:i + kernel_height, j:j + kernel_width, c]
              img_conv[i, j, c] = np.sum(region * kernel)

  # Clip output for display
  img_conv = np.clip(img_conv, 0, 1)
  return img_conv.squeeze()  # remove single channel if grayscale


# === FFT ===

# === HELPER FUNCTIONS ===
def load_image(image_path: str) -> np.ndarray:

    # Load the image using PIL and convert to grayscale
    image = Image.open(image_path).convert('L') #('L' mode = 8-bit grayscale)

    # Convert to NumPy array and scale to [0, 1]
    image_array = np.array(image, dtype=np.float64) / 255.0

    return image_array

def load_color_image(image_path: str) -> np.ndarray:
    # Load an RGB image as float64 in [0,1], shape (H, W, 3).
    
    image = Image.open(image_path).convert('RGB')
    image_array = np.array(image, dtype=np.float64) / 255.0
    return image_array


def dft2_from_fft1(image_array: np.ndarray) -> np.ndarray:

    # Apply FFT along rows (axis=1)
    fft_rows = np.fft.fft(image_array, axis=1)

    # Apply FFT along columns (axis=0)
    fft_2d = np.fft.fft(fft_rows, axis=0)

    return fft_2d


def visualize_spectrum_phase(F: np.ndarray):

    # Compute magnitude and phase
    magnitude = np.abs(F)
    phase = np.angle(F)

    # Apply log transform for better visualization
    log_magnitude = np.log(1 + magnitude)

    # Shift zero-frequency component to the center
    log_magnitude_shifted = np.fft.fftshift(log_magnitude)
    phase_shifted = np.fft.fftshift(phase)

   # === DEFINE KERNEL ===
def generate_gaussian_kernel(size, sigma): 
    """
    Generates kernel function
    Args: sigma = STD of Gaussian Distribution 
    Returns: kenel_2D (2D numpy array) 
    """
    if size % 2 == 0:
        raise ValueError("Kernel size must be an odd integer.")

    # Create 1D Gaussian kernels
    x = np.linspace(-(size // 2), size // 2, size)
    gaussian_1d = np.exp(-(x**2) / (2 * sigma**2))
    gaussian_1d /= np.sum(gaussian_1d) # Normalize

    # Create 2D kernel by outer product
    kernel_2d = np.outer(gaussian_1d, gaussian_1d)

    return kernel_2d






