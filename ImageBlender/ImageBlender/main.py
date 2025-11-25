# === MAIN MODULE / EXECUTION FUNCTION ===
import time
import tkinter as tk
from gui import ROIAnnotation

if __name__ == "__main__":

    # START CLOCK TO RECORD SPEED OF PROGRAM

    # ORCHESTRATE PYRAMID BLENDING

    # CALL GUI TO GENERATE MASK
    root = tk.Tk()
    app = ROIAnnotation(root)
    root.mainloop()

    # REPORT TIME OF PROGRAM
