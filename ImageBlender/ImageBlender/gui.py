# GUI CODE
import os
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageDraw
"""
PURPOSE: Opens foreground image, gives user the ability to 
select origin of interest and generate black & white mask" 
"""

# === DEFINE CLASSES ===
class ROIAnnotation:
    def __init__(self, root):
        self.root=root
        self.root.title("ROI Annotator")

        #define variables
        self.loaded_image=None
        self.tk_image=None
        self.roi_shape=tk.StringVar(value="rectangle")
        self.start_x=None
        self.start_y=None
        self.current_preview=None
        self.final_roi=None

        #build UI
        self.build_ui()

    # BUILD UI LAYOUT
    def build_ui(self): 
        # Define Buttons


    # ROI DRAWING LOGIC
    def move_mouse_down(self, event): 

    def move_mouse_up(self, event):

    def mouse_drag(self, event): # allows for "free form" ROI

    # CREATE AND SAVE MASK
    def save_mask(self): 


# TODO; DO I NEED TO CONVERT TO BINARY OR LEAVE [0, 255] SCALE


