import numpy as np
from PIL import Image
from helper import conv2, generate_gaussian_kernel

def downsample(image):
    # Nearest neighbor downsampling by factor of 2
    return image[::2, ::2, ...]

def upsample(image, target_shape):
    # Nearest neighbor upsampling by factor of 2
    up = np.repeat(np.repeat(image, 2, axis=0), 2, axis=1)
    th, tw = target_shape[0], target_shape[1]

    if up.ndim == 3:
        up_cropped = up[:th, :tw, ...] 
    else:
        up_cropped = up[:th, :tw]
    return up_cropped

def max_pyr_layers(height, width):
    layers = 1
     # We can keep halving while both dimensions >= 2
    while min(height, width) >= 2:
        height = (height + 1) // 2
        width = (width + 1) // 2
        layers += 1

    return layers

def ComputePyr(input_image, num_layers, gauss_size = 5, gauss_sigma = 2):
    # Compute Gaussian and Laplacian pyramids for a single image.
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

        # Upsample back to current size for Laplacian
        up = upsample(next_img, current.shape)

        # Laplacian = current Gaussian - upsampled next Gaussian
        lap = current - up
        lPyr.append(lap)

        current = next_img

    # Final (coarsest) Gaussian level
    gPyr.append(current)
    # For reconstruction, we treat the last Laplacian level as the coarsest Gaussian
    lPyr.append(current)
    
    return gPyr, lPyr


def reconstruct_from_laplacian(lPyr):
    """
    Reconstruct an image from its Laplacian pyramid.
    Assumes lPyr[-1] is the coarsest Gaussian image.
    """
    current = lPyr[-1]
    # Go from coarsest-1 back to finest
    for level in reversed(lPyr[:-1]):
        current = upsample(current, level.shape) + level
    # Clip to valid range
    return np.clip(current, 0.0, 1.0)

def laplacian_pyramid_blend(src, tgt, mask, num_layers=5, gauss_size=5, gauss_sigma=2):
    """
    Perform Laplacian pyramid blending of two images using a mask.

    Args:
        src: source image (numpy array, HxW or HxWxC) in [0,1] or [0,255]
        tgt: target image (same size as src)
        mask: mask image (same size as src), ideally in [0,1], white=source
        num_layers: number of pyramid levels
    Returns:
        blended: blended image as numpy array in [0,1]
    """
    # Ensure float64
    src = src.astype(np.float64)
    tgt = tgt.astype(np.float64)
    mask = mask.astype(np.float64)

    # Normalize ranges if needed
    if src.max() > 1.0:
        src /= 255.0
    if tgt.max() > 1.0:
        tgt /= 255.0
    if mask.max() > 1.0:
        mask /= 255.0

    # Ensure shapes match
    #assert src.shape == tgt.shape == mask.shape, "Source, target, and mask must have the same shape."

    # Build pyramids
    gSrc, lSrc = ComputePyr(src, num_layers, gauss_size, gauss_sigma)
    gTgt, lTgt = ComputePyr(tgt, num_layers, gauss_size, gauss_sigma)
    gMask, _   = ComputePyr(mask, num_layers, gauss_size, gauss_sigma)

    # Blend per level
    blended_pyr = []
    for l_s, l_t, g_m in zip(lSrc, lTgt, gMask):
        # Make sure mask can broadcast correctly for RGB images
        if l_s.ndim == 3 and g_m.ndim == 2:
            g_m = g_m[..., np.newaxis]
        blended_level = g_m * l_s + (1.0 - g_m) * l_t
        blended_pyr.append(blended_level)

    # Reconstruct from blended Laplacian pyramid
    blended = reconstruct_from_laplacian(blended_pyr)
    return blended


def embed_source_and_mask_in_background(src, mask, target_shape, top_left=None):
    """
    Embed an RGB (or grayscale) src and its single-channel mask into
    a black background of size target_shape (H,W,3 or H,W).
    """

    H_t, W_t = target_shape[0], target_shape[1]
    H_s, W_s = src.shape[0], src.shape[1]

    # Ensure spatial dims of mask match src initially
    if mask.shape[:2] != (H_s, W_s):
        raise ValueError(
            f"Mask spatial size must match source. Got src {src.shape}, mask {mask.shape}"
        )

    # --- If source is larger than target, resize BOTH src and mask down to fit ---
    if H_s > H_t or W_s > W_t:
        scale = min(H_t / H_s, W_t / W_s)
        new_H = max(1, int(H_s * scale))
        new_W = max(1, int(W_s * scale))

        # Prepare src for resizing
        src_img = src.copy()
        if src_img.max() <= 1.0:
            src_img = (src_img * 255.0)
        src_img = np.clip(src_img, 0, 255).astype(np.uint8)

        if src_img.ndim == 2:
            pil_src = Image.fromarray(src_img, mode="L")
        else:
            pil_src = Image.fromarray(src_img)  # RGB

        # Prepare mask for resizing
        mask_img = mask.copy()
        if mask_img.max() <= 1.0:
            mask_img = (mask_img * 255.0)
        mask_img = np.clip(mask_img, 0, 255).astype(np.uint8)
        # ensure 2D for mask
        if mask_img.ndim == 3:
            mask_img = mask_img[..., 0]
        pil_mask = Image.fromarray(mask_img, mode="L")

        pil_src = pil_src.resize((new_W, new_H), Image.BILINEAR)
        pil_mask = pil_mask.resize((new_W, new_H), Image.BILINEAR)

        src = np.asarray(pil_src).astype(np.float64)
        mask = np.asarray(pil_mask).astype(np.float64)

        if src.max() > 1.0: src /= 255.0
        if mask.max() > 1.0: mask /= 255.0

        H_s, W_s = src.shape[0], src.shape[1]

    # --- Create backgrounds ---
    if len(target_shape) == 3:
        # RGB background
        src_bg = np.zeros(target_shape, dtype=src.dtype)
    else:
        src_bg = np.zeros(target_shape, dtype=src.dtype)

    mask_bg = np.zeros((H_t, W_t), dtype=mask.dtype)

    # Position (center by default)
    if top_left is None:
        row = (H_t - H_s) // 2
        col = (W_t - W_s) // 2
    else:
        row, col = top_left

    row = max(0, min(row, H_t - H_s))
    col = max(0, min(col, W_t - W_s))

    if src.ndim == 2:
        src_bg[row:row + H_s, col:col + W_s] = src
    else:
        src_bg[row:row + H_s, col:col + W_s, :] = src

    mask_bg[row:row + H_s, col:col + W_s] = mask

    return src_bg, mask_bg


def save_image(img, path):
    img = img.astype(np.float64)
    if img.max() <= 1.0:
        img = img * 255.0
    img = np.clip(img, 0, 255).astype(np.uint8)

    if img.ndim == 2:
        Image.fromarray(img, mode="L").save(path)
    else:
        Image.fromarray(img, mode="RGB").save(path)

