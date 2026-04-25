#%%
import imageio
from os.path import exists
import os
import numpy as np

images = []

# Enter file path here
path = os.path.join(os.getcwd(), 'state_space_frames_transparent')

# Set total number of images here
n_frames = 300
# Set video FPS here
fpsec = 20

# Set video file name here (change to .gif to save a gif file instead of mp4)
file_name = 'end_anim.gif'

for i in range(1,n_frames,1):
    if exists(os.path.join(path, str(i)+'.png')):
        images.append(imageio.imread(os.path.join(path, str(i)+'.png')))
        print(i)

imageio.mimsave(os.path.join(path,file_name), images, fps = fpsec, loop=0)




# Ignore this code I don't use it but you can save videos using this if you want.
# #%%
# from moviepy.editor import *
# clip = VideoFileClip('Sub-Level_Example.gif')
# clip.write_videofile("Sub-Level_Example.mp4", fps=10)