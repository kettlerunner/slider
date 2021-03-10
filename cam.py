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
current_width = 0
current_height = 0

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

current_img = cv2.imread(filenames[random.randrange(0, len(filenames))])
previous_img = cv2.imread(filenames[random.randrange(0, len(filenames))])
scale = min(max_width / previous_img.shape[1],
                        max_height / previous_img.shape[0])
scaled_img = cv2.resize(previous_img, (int(previous_img.shape[1] * scale), int(previous_img.shape[0] * scale)))
current_width = scaled_img.shape[1] 
current_height = scaled_img.shape[0] 
slide = insert_photo(bg_frame.copy(), scaled_img)
cv2.imshow('Cam', slide)
while(True): 
    x += 1
    j += 1
    print(x)
    if x > 2000:
        x = 0
    elif x == 1:
        current_width = scaled_img.shape[1] 
        current_height = scaled_img.shape[0] 
        slide = insert_photo(bg_frame.copy(), scaled_img)
        cv2.imshow('Cam', slide)
    elif x == 1800:
        previous_img = current_img.copy()
        current_img = cv2.imread(filenames[random.randrange(0, len(filenames))])
        buffer = requests.get(url).text
        server_filenames = json.loads(str(buffer)).get('files')
        local_filenames = glob.glob(os.path.join(path, "*"))
        for s in server_filenames:
            if s not in [i.replace(local_base, "") for i in local_filenames]:
                urllib.request.urlretrieve(image_locations + s.replace(" ", "%20"), local_base + s.replace(" ", "%20"))
                filenames = glob.glob(os.path.join(path, "*"))
        if current_img.shape[1] > max_width or current_img.shape[0] > max_height:
            scale = min(max_width / current_img.shape[1], max_height / current_img.shape[0])
            scaled_img = cv2.resize(current_img, (int(current_img.shape[1] * scale), int(current_img.shape[0] * scale))).copy() 
        else:
            scaled_img = current_img.copy()
        next_width = scaled_img.shape[1] 
        next_height = scaled_img.shape[0]
    elif x > 1900:
        current_width -= 1
        current_height -= 1 
        fade_img = cv2.resize(previous_img, (current_width, current_height))
        fade_img2 = current_img.copy()
        slide = insert_photo(bg_frame.copy(), fade_img)
        slide2 = insert_photo(bg_frame.copy(), fade_img2)
        image_new = cv2.addWeighted(slide2, (x-1900)/100, slide, 1 - (x-1900)/100, 0)
        cv2.imshow('Cam', image_new)
        
    if cv2.waitKey(1) & 0xFF == ord('s'): 
        break
 
                       
cv2.destroyAllWindows()
