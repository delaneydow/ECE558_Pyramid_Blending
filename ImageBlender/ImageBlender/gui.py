# GUI CODE
import os
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageDraw
from helper import load_image
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
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Button(control_frame, text="Load Image", command=self.load_image).pack(side=tk.LEFT, padx=5)
        ttk.Label(control_frame, text="ROI Shape:").pack(side=tk.LEFT, padx=(10, 2))
        ttk.OptionMenu(control_frame, self.roi_shape, "rectangle", "rectangle", "ellipse").pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Save Mask", command=self.save_mask).pack(side=tk.LEFT, padx=5)

        # Canvas
        self.canvas = tk.Canvas(self.root, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind defined events (mouse logic)
        self.canvas.bind("<ButtonPress-1>", self.move_mouse_down)
        self.canvas.bind("<B1-Motion>", self.mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.move_mouse_up)

    def load_image(self):
        file_path = filedialog.askopenfilename()  # no filetypes filter so can run on Mac
        # file_path = filedialog.askopenfilename(
        #     filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.tif;*.bmp")]
        # )
        if not file_path:
            return

        # Load numpy version (for later processing)
        self.image_array = load_image(file_path)   # using helper

         # Load Pillow version for GUI display
        pil_image = Image.open(file_path).convert("RGB")   # show in color or "L"
        self.loaded_image = pil_image                      # keep a reference

        # Convert to Tkinter image
        self.tk_image = ImageTk.PhotoImage(pil_image)

        # Update canvas
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.config(width=pil_image.width, height=pil_image.height)

        # Reset ROI
        self.final_roi = None


    # ROI DRAWING LOGIC
    def move_mouse_down(self, event): 
        # Define directions
        self.start_x = event.x
        self.start_y = event.y

        # Remove old preview
        if self.current_preview:
            self.canvas.delete(self.current_preview)

    def move_mouse_up(self, event):
        # Final ROI stored as (x1, y1, x2, y2)
        self.final_roi = (
            min(self.start_x, event.x),
            min(self.start_y, event.y),
            max(self.start_x, event.x),
            max(self.start_y, event.y)
        )
        print("ROI selected:", self.final_roi)

    def mouse_drag(self, event): # allows for "free form" ROI
        # Remove previous preview shape
        if self.current_preview:
            self.canvas.delete(self.current_preview)

        # Draw new preview shape
        if self.roi_shape.get() == "rectangle":
            self.current_preview = self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline="yellow", width=2
            )
        else:  # ellipse, provides flexibility
            self.current_preview = self.canvas.create_oval(
                self.start_x, self.start_y, event.x, event.y,
                outline="yellow", width=2
            )

    # CREATE AND SAVE MASK
    def save_mask(self): 
        if self.loaded_image is None:
            print("No image loaded.")
            return
        if self.final_roi is None:
            print("No ROI selected.")
            return

        # Create a black mask
        mask = Image.new("L", self.loaded_image.size, 0)  # "L" = grayscale [0..255]
        draw = ImageDraw.Draw(mask)

        x1, y1, x2, y2 = self.final_roi

        if self.roi_shape.get() == "rectangle":
            draw.rectangle((x1, y1, x2, y2), fill=255)
        else:
            draw.ellipse((x1, y1, x2, y2), fill=255)

        # Ask where to save
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Mask", "*.png")]
        )
        if save_path:
            mask.save(save_path)
            print("Mask saved to:", save_path)





