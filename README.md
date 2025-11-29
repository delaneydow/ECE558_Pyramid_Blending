# ECE558_Pyramid_Blending
ECE 558 Final Project

Welcome to Pyramid Blending! To get started, please review the following: 

1. Program Structure
   The main contents are found in the ImageBlender/ImageBlender folder of the main repository. Within this folder, the main files of the program are gui.py, helper.py, main.py, and pyramid.py.

   a) gui.py

   This file contains the GUI code. It creates a class for the GUI that is instantiated in main, as well as mouse and user-behavior functionality. The GUI allows for the user to select the image annotation from the source image, and saves the annotation either as an ellipse or a rectangle. 

   b) helper.py

  This file contains any helper functions, as well as code that may be re-used across different files. Examples of functions included in this file include an image loader function, or defining the gaussian kernel. This file is intended to assist in modularizing the program. 

   c) main.py

   This file is the orchestration of all the differet pieces of the code. It runs the GUI to assist in the user-interactivity piece, mask generation, and calls the blending functions. It also times the different pieces of the program for run-time analysis. 

   d) pyramid.py 

   This file orchestrates the Gaussian and Laplacian pyramid blending, then outputs the final blended image. 

3. Implementation Details

   1) Clone Repository
   2) Confirm that you would like to save images to the /Images directory. It already comes with three different image pairs, labeled Source[x], target[x], etc. If you would like to change this directory, update the given directory in line 12 of the main.py function under IMAGES_DIR = "images". 
   3) Run main.py function, and the GUI will load to enable you to select the source image, the shape of the annotation, and to save the mask. 
  
  
      <img width="392" height="306" alt="image" src="https://github.com/user-attachments/assets/4d557b7e-a374-46ae-97b2-abd88a682c8d" />

    4) The program will then generate the blended images from the pairs in your /images folder. An example of the target, source, mask, and blend output is below.

5. Examples

   The folder ImageBlender/ImageBlender/images contains examples of the image blending results. There are three examples, or which there is a source image, a target image, a mask image (an annotation taken from the source image), and the blending result.

   Source:
   
   <img width="480" height="396" alt="image" src="https://github.com/user-attachments/assets/839225de-1ff8-47b4-b9ee-6035055a8cc1" />


   Mask:
   
   <img width="480" height="396" alt="image" src="https://github.com/user-attachments/assets/e486befc-ae8a-4380-8cd2-59fd68e7363b" />


   Target:
   
   <img width="465" height="432" alt="image" src="https://github.com/user-attachments/assets/dd3ad104-5131-47a4-a4fe-2cfa6773cf9f" />


   Blend:
   
   <img width="465" height="432" alt="image" src="https://github.com/user-attachments/assets/282d9861-9a4b-4a47-8277-f084c8483cce" />

