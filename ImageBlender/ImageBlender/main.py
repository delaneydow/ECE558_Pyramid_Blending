# main.py

import sys
import numpy as np
import matplotlib.pyplot as plt

from helper import load_image
from pyramid import ComputePyr


def visualize_pyramids(gPyr, lPyr):
    num_layers = len(gPyr)

    plt.figure(figsize=(12, 4 * num_layers))

    for i in range(num_layers):
        # --- Gaussian level ---
        plt.subplot(num_layers, 2, 2 * i + 1)
        g_img = gPyr[i]
        if g_img.ndim == 2:  # grayscale
            plt.imshow(g_img, cmap='gray')
        else:  # color
            plt.imshow(g_img)
        plt.title(f"Gaussian Level {i} (shape={g_img.shape})")
        plt.axis("off")

        # --- Laplacian level ---
        plt.subplot(num_layers, 2, 2 * i + 2)
        l_img = lPyr[i]
        # For visualization, shift Laplacian to [0,1] range
        l_vis = l_img - l_img.min()
        if l_vis.max() > 0:
            l_vis = l_vis / l_vis.max()
        if l_vis.ndim == 2:
            plt.imshow(l_vis, cmap='gray')
        else:
            plt.imshow(l_vis)
        plt.title(f"Laplacian Level {i} (shape={l_img.shape})")
        plt.axis("off")

    plt.tight_layout()
    plt.show()


def main():
    image_path = './image.png'
    img = load_image(image_path)

    print(f"Input image shape: {img.shape}")

    num_layers = 4

    gPyr, lPyr = ComputePyr(img, num_layers)

    print("\nGaussian Pyramid Shapes:")
    for i, g in enumerate(gPyr):
        print(f"  Level {i}: {g.shape}")

    print("\nLaplacian Pyramid Shapes:")
    for i, l in enumerate(lPyr):
        print(f"  Level {i}: {l.shape}")

    visualize_pyramids(gPyr, lPyr)


if __name__ == "__main__":
    main()

