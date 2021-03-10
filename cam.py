import cv2 
import numpy as np
import glob
import os
import random
import requests
import json
import urllib

bg_frame = cv2.imread("frame.jpg")
cv2.namedWindow('Cam', cv2.WINDOW_FREERATIO)
cv2.setWindowProperty('Cam', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def insert_photo(bg_image, insert_image):
  bg_width = bg_image.shape[1]
  bg_height = bg_image.shape[0]
  in_width = insert_image.shape[1]
  in_height = insert_image.shape[0]
  
  left = int((bg_width - in_width)/2)
  top = int((bg_height - in_height)/2)
  
  overlay_image = bg_image.copy()
  overlay_image[top:top+in_height, left:left+in_width] = insert_image
  
  return overlay_image

url = "https://dancrouse.com/slider"
local_base = "images/"
image_locations = "https://dancrouse.com/static/img/slider/"
framename = "slideshow"
path = "images/"

max_width = 800
max_height = 480
scale = 0.0
alpha = 1.0
blurr = 0.0

filenames = glob.glob(os.path.join(path, "*"))
x = 0
j = 0

previous_img = cv2.imread(filenames[random.randrange(0, len(filenames))])
scale = min(max_width / previous_img.shape[1],
                        max_height / previous_img.shape[0])
scaled_img = cv2.resize(previous_img, (int(previous_img.shape[1] * scale), int(previous_img.shape[0] * scale)))
slide = insert_photo(bg_frame.copy(), scaled_img)
cv2.imshow('Cam', slide)
while(True): 
    x += 1
    j += 1
    print(x)
    if x > 2000:
        buffer = requests.get(url).text
        server_filenames = json.loads(str(buffer)).get('files')
        local_filenames = glob.glob(os.path.join(path, "*"))
        for s in server_filenames:
            if s not in [i.replace(local_base, "") for i in local_filenames]:
                print(s)
                urllib.request.urlretrieve(
                    image_locations + s.replace(" ", "%20"), local_base + s.replace(" ", "%20"))
                filenames = glob.glob(os.path.join(path, "*"))
        filename = filenames[random.randrange(0, len(filenames))]
        print(filename)
        previous_img = cv2.imread(filename)
        if previous_img.shape[1] > max_width or previous_img.shape[0] > max_height:
            scale = min(max_width / previous_img.shape[1], max_height / previous_img.shape[0])
            scaled_img = cv2.resize(previous_img, (int(previous_img.shape[1] * scale), int(previous_img.shape[0] * scale))).copy()
        else:
            scaled_img = previous_img.copy()
        x = 0
        slide = insert_photo(bg_frame.copy(), scaled_img)
        cv2.imshow('Cam', slide)
    elif x > 1500:
        scaled_img = cv2.resize(scaled_img, (scaled_img.shape[1] - 1, scaled_img.shape[0] - 1))
        slide = insert_photo(bg_frame.copy(), scaled_img)
        cv2.imshow('Cam', slide)
                      
    if cv2.waitKey(1) & 0xFF == ord('s'): 
        break
 
video.release() 
result.release() 
cv2.destroyAllWindows()
