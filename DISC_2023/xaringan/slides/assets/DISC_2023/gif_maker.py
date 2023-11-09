#%%
import imageio
from os.path import exists
import os
import numpy as np

images = []

# Enter file path here
path = os.path.join(os.getcwd(), 'sl_anim')

# Set total number of images here
n_frames = 900

# Set video FPS here
fpsec = 30

# Set video file name here (change to .gif to save a gif file instead of mp4)
file_name = 'test.gif'

for i in range(1,n_frames,4):
    if exists(os.path.join(path, 'sl_pers_'+str(i)+'.jpg')):
        images.append(imageio.imread(os.path.join(path, 'sl_pers_'+str(i)+'.jpg')))
        print(i)

imageio.mimsave(os.path.join(path,file_name), images, fps = fpsec)




# Ignore this code I don't use it but you can save videos using this if you want.
# #%%
# from moviepy.editor import *
# clip = VideoFileClip('Sub-Level_Example.gif')
# clip.write_videofile("Sub-Level_Example.mp4", fps=10)

#%%
from PIL import Image

# Open the image
for i in range(1,901):
    input_image_path = os.path.join(path, 'sl_pers_'+str(i)+'.jpg')
    output_image_path = os.path.join(path, 'sl_pers_'+str(i)+'.jpg')
    image = Image.open(input_image_path)

    # Set the new DPI value (e.g., 300 DPI)
    frac = 0.8
    new_dpi = (int(frac*3600),int(frac*1340))

    # Change the DPI of the image
    # image.info["dpi"] = new_dpi
    image = image.resize(new_dpi)
    # Save the modified image
    image.save(output_image_path, dpi=new_dpi)

    # Close the image
    image.close()
    print(i)