# === MAIN MODULE / EXECUTION FUNCTION ===
import time
import tkinter as tk
from gui import ROIAnnotation

if __name__ == "__main__":

    # START CLOCK TO RECORD SPEED OF PROGRAM
    program_start = time.perf_counter()

    # CALL GUI TO GENERATE MASK
    gui_start = time.perf_counter()
    root = tk.Tk()
    app = ROIAnnotation(root)
    root.mainloop()
    gui_end = time.perf_counter()
    print(f"GUI time: {gui_end - gui_start:.3f} seconds")

    # ORCHESTRATE PYRAMID BLENDING
    # Example: iterate over 3 required photos - can change structure of this later
    pyramid_times = []
    for idx, photo_path in enumerate(["photo1.png", "photo2.png", "photo3.png"], 1):
        start = time.perf_counter()

    # call blending function 
    end = time.perf_counter()
    elapsed = end - start
    pyramid_times.append(elapsed)
    print(f"Pyramid blending for photo {idx}: {elapsed:.3f} seconds")
     

    # REPORT TOTAL TIME OF PROGRAM
    program_end = time.perf_counter()
    print(f"Total program time: {program_end - program_start:.3f} seconds")
