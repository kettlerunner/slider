import cv2 
import numpy as np


video = cv2.VideoCapture(0) 

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
