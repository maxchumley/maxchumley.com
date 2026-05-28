#%%
import imageio
from os.path import exists
import os
import numpy as np

images = []

# Enter file path here
path = os.path.join(os.getcwd(), 'random_detuning_avg_ATA')

save_path = os.getcwd()

# Set total number of images here
n_frames = 78
# Set video FPS here
fpsec = 5

# Set video file name here (change to .gif to save a gif file instead of mp4)
file_name = 'ATA_anim.gif'

for i in range(0,n_frames,1):
    if exists(os.path.join(path, f'{i}.png')):
        img = imageio.imread(os.path.join(path, f'{i}.png'))
        # Downsample the image by a factor of 2
        img_small = img[::1, ::1]
        images.append(img_small)
        print(i)

imageio.mimsave(os.path.join(save_path,file_name), images, fps = fpsec, loop=0)




# Ignore this code I don't use it but you can save videos using this if you want.
# #%%
# from moviepy.editor import *
# clip = VideoFileClip('Sub-Level_Example.gif')
# clip.write_videofile("Sub-Level_Example.mp4", fps=10) 

#%%

import imageio
import numpy as np
from os.path import exists
import os

images = []

path = os.path.join(os.getcwd(), 'collocation_frames')
save_path = os.getcwd()
n_frames = 51
fps = 5

file_name = 'eig_example.mp4'

phi_p = np.linspace(0, 2, n_frames)

for i in np.arange(0, n_frames-1, 1):
    img_path = os.path.join(path, f'collocation_N{i}.png')
    if exists(img_path):
        img = imageio.imread(img_path)

        # Convert to RGB if needed
        if img.ndim == 2:  # grayscale
            img = np.stack([img]*3, axis=-1)
        elif img.shape[2] == 4:  # RGBA
            img = img[:, :, :3]  # drop alpha channel

        images.append(img)
        print(f"Frame {i} added")


# Write MP4
writer = imageio.get_writer(os.path.join(save_path, file_name), fps=fps, codec='libx264')
for frame in images:
    writer.append_data(frame)
writer.close()