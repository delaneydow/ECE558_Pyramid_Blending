# === MAIN MODULE / EXECUTION FUNCTION ===
import time
import tkinter as tk
from gui import ROIAnnotation
import os
from pyramid import laplacian_pyramid_blend, embed_source_and_mask_in_background, save_image
import numpy as np
import matplotlib.pyplot as plt
from helper import load_image, load_color_image
from pyramid import ComputePyr

IMAGES_DIR = "images"


if __name__ == "__main__":

    # START CLOCK TO RECORD SPEED OF PROGRAM
    program_start = time.perf_counter()

    # --- GUI: create a mask if you want to generate a new one ---
    gui_start = time.perf_counter()
    root = tk.Tk()
    app = ROIAnnotation(root)
    root.mainloop()
    gui_end = time.perf_counter()
    print(f"GUI time: {gui_end - gui_start:.3f} seconds")

    pyramid_times = []

    for idx in range(1, 4):
        start = time.perf_counter()

        src_path = os.path.join(IMAGES_DIR, f"source{idx}.png")
        tgt_path = os.path.join(IMAGES_DIR, f"target{idx}.png")
        msk_path = os.path.join(IMAGES_DIR, f"mask{idx}.png")

        # Load grayscale [0,1]
        # src = load_image(src_path)
        # tgt = load_image(tgt_path)
        # Load color
        src = load_color_image(src_path)
        tgt = load_color_image(tgt_path)
        mask = load_image(msk_path)

        if src.shape[0:2] != mask.shape[0:2]:
            raise ValueError(
                f"For pair {idx}, source and mask must match spatially. "
                f"Got src {src.shape}, mask {mask.shape}"
            )

        if src.shape[0:2] != tgt.shape[0:2]:
            print(f"Adjusting and embedding source{idx} and its mask into background to match target size.")
            src, mask = embed_source_and_mask_in_background(src, mask, tgt.shape)

        if src.shape != tgt.shape:
            raise ValueError(
                f"After embedding, source and target must match exactly. "
                f"Got src {src.shape}, tgt {tgt.shape}"
            )

        if mask.shape[0:2] != tgt.shape[0:2]:
            raise ValueError(
                f"After embedding, mask must match target spatially. "
                f"Got mask {mask.shape}, target {tgt.shape}"
            )


        blended = laplacian_pyramid_blend(src, tgt, mask, num_layers=7, gauss_size=7, gauss_sigma=2.5)

        out_path = os.path.join(IMAGES_DIR, f"blend{idx}.png")
        save_image(blended, out_path)
        print(f"Saved blended result for pair {idx} to {out_path}")

        end = time.perf_counter()
        elapsed = end - start
        pyramid_times.append(elapsed)
        print(f"Pyramid blending for pair {idx}: {elapsed:.3f} seconds")

    program_end = time.perf_counter()
    print(f"Total program time: {program_end - program_start:.3f} seconds")
