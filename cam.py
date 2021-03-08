import cv2 
import numpy as np
import glob
import os
import random


url = "https://dancrouse.com/slider"
local_base = "images/"
image_locations = "https://dancrouse.com/static/img/slider/"
framename = "slideshow"
path = "images/"

max_width = 600
max_height = 500
scale = 0.0
alpha = 1.0
blurr = 0.0

filenames = glob.glob(os.path.join(path, "*"))

while(True): 
    previous_img = cv2.imread(filenames[random.randrange(0, len(filenames))])
    if previous_img.shape[1] > max_width or previous_img.shape[0] > max_height:
        scale = min(max_width / previous_img.shape[1],
                    max_height / previous_img.shape[0])
        previous_img = cv2.resize(
            previous_img, (int(previous_img.shape[1] * scale), int(previous_img.shape[0] * scale)))
    cv2.imshow('Cam', previous_img)
                      
    if cv2.waitKey(1) & 0xFF == ord('s'): 
        break
 
video.release() 
result.release() 
cv2.destroyAllWindows()




while True:
    p_scale = 0
    x = 0
    while True:
        if x == 0:
            buffer = requests.get(url).text
            server_filenames = json.loads(str(buffer)).get('files')
            local_filenames = glob.glob(os.path.join(path, "*"))
            for s in server_filenames:
                if s not in [i.replace(local_base, "") for i in local_filenames]:
                    print(s)
                    urllib.request.urlretrieve(
                        image_locations + s.replace(" ", "%20"), local_base + s.replace(" ", "%20"))
                    filenames = glob.glob(os.path.join(path, "*"))
            if j == 0:
                previous_img = cv2.imread(filenames[random.randrange(0, len(filenames))])
                if previous_img.shape[1] > max_width or previous_img.shape[0] > max_height:
                    scale = min(max_width / previous_img.shape[1],
                                max_height / previous_img.shape[0])
                    previous_img = cv2.resize(
                        previous_img, (int(previous_img.shape[1] * scale), int(previous_img.shape[0] * scale)))
