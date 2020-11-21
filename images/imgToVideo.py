import cv2

import numpy as np
import os
 
import re
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

img_array = []
images = [img for img in sorted_alphanumeric(os.listdir(".")) if img.endswith(".pgm")]

for image in images:
    #print(image)
    img = cv2.imread(os.path.join(".", image))
    scale_percent = 1000 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100) 
    dim = (width, height)
    img = cv2.resize( img, dim, interpolation=cv2.INTER_NEAREST)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 

out = cv2.VideoWriter('project.avi', 0 , 60, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()

#import subprocess
#result = subprocess.run('ffmpeg -i project.avi -b 800k zout.mp4')
#print(result)

'''
ffmpeg -framerate 300 -i out%d.pgm -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p -vf "scale=10*iw:-1:flags=neighbor" 0outputC.mp4
ffmpeg -i 0outputC.mp4 -vf "setpts=0.5*PTS" 00out.mp4
'''