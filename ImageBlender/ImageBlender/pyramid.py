import numpy as np
from helper import conv2, generate_gaussian_kernel

def downsample(image):
    return image[::2, ::2, ...]

def upsample(image, target_shape):
    up = np.repeat(np.repeat(image, 2, axis=0), 2, axis=1)
    th, tw = target_shape[0], target_shape[1]

    if up.ndim == 3:
        up_cropped = up[:th, :tw, ...] 
    else:
        up_cropped = up[:th, :tw]
    return up_cropped

def max_pyr_layers(height, width):
    layers = 1

    while min(height, width) >= 2:
        height = (height + 1) // 2
        width = (width + 1) // 2
        layers += 1

    return layers

def ComputePyr(input_image, num_layers, gauss_size = 5, gauss_sigma = 1):
    pad_mode = 'reflect'
    img = input_image.astype(np.float64)
    if img.max() > 1.0:
        img /= 255.0

    h, w = img.shape[0], img.shape[1]
    max_layers = max_pyr_layers(h, w)
    if num_layers > max_layers:
        num_layers = max_layers
    
    g_kernel = generate_gaussian_kernel(size=gauss_size, sigma=gauss_sigma)
    gPyr = []
    lPyr = []

    current = img

    for _ in range(num_layers - 1):
        gPyr.append(current)
        blurred = conv2(current, g_kernel, pad_mode)
        next_img = downsample(blurred)
        up = upsample(next_img, current.shape)

        # Laplacian = current Gaussian - upsampled next Gaussian
        lap = current - up
        lPyr.append(lap)

        current = next_img

    gPyr.append(current)
    lPyr.append(current)
    
    return gPyr, lPyr