import cv2 
import numpy as np
import glob


video = cv2.VideoCapture(0) 

url = "https://dancrouse.com/slider"
local_base = "images/"
image_locations = "https://dancrouse.com/static/img/slider/"
framename = "slideshow"
path = "images/"

filenames = glob.glob(os.path.join(path, "*"))

for filename in filenames:
  print(filename)

while(True): 
    ret, frame = video.read() 
    if ret == True:  
        cv2.imshow('Cam', frame)
                      
        if cv2.waitKey(1) & 0xFF == ord('s'): 
            break
    else: 
        break
  
 
video.release() 
result.release() 
cv2.destroyAllWindows() 
