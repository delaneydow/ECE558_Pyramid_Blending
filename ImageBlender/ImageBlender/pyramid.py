import numpy as np

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

def ComputePyr(input_image, num_layers):
    gPyr = []
    lPyr = []
    
    return gPyr, lPyr