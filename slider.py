import cv2
import numpy as np
import glob
import os
import random
import requests
import json
import urllib

url = "https://dancrouse.com/slider"
local_base = "images/"
image_locations = "https://dancrouse.com/static/img/slider/"
framename = "slideshow"
path = "images/"

filenames = glob.glob(os.path.join(path, "*"))

j = 0
cv2.namedWindow(framename, cv2.WINDOW_FREERATIO)
frame = cv2.imread("frame.jpg")
cv2.imshow(framename, frame)
max_width = 800
max_height = 480
scale_x = 0.0
scale_y = 0.0
scale = 0.0
alpha = 1.0
blurr = 0.0

while True:
    p_scale = 0
    while x in range(0, 3000):
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
                current_img = cv2.imread(filenames[random.randrange(0, len(filenames))])
                if current_img.shape[1] > max_width or current_img.shape[0] > max_height:
                    scale = min(max_width / current_img.shape[1], max_height / current_img.shape[0])
                    current_img = cv2.resize(
                        current_img, (int(current_img.shape[1] * scale), int(current_img.shape[0] * scale)))
                next_img = cv2.imread(filenames[random.randrange(0, len(filenames))])
                if next_img.shape[1] > max_width or next_img.shape[0] > max_height:
                    scale = min(max_width / next_img.shape[1], max_height / next_img.shape[0])
                    next_img = cv2.resize(
                        next_img, (int(next_img.shape[1] * scale), int(next_img.shape[0] * scale)))
            else:
                previous_img = current_img.copy()
                current_img = next_img.copy()
                next_img = cv2.imread(filenames[random.randrange(0, len(filenames))])
                if next_img.shape[1] > max_width or next_img.shape[0] > max_height:
                    scale = min(max_width / next_img.shape[1], max_height / next_img.shape[0])
                    next_img = cv2.resize(
                        next_img, (int(next_img.shape[1] * scale), int(next_img.shape[0] * scale)))
            j += 1
            current_frame = frame.copy()
            start_x = int((800 - current_img.shape[1])/2)
            start_y = int((480 - current_img.shape[0])/2)
            current_frame[start_y:start_y + current_img.shape[0],
                          start_x:start_x + current_img.shape[1]] = current_img
            cv2.imshow(framename, current_frame)
        elif x > 2500:
            current_frame = frame.copy()
            start_x = int((800 - current_img.shape[1])/2)
            start_y = int((480 - current_img.shape[0])/2)
            current_frame[start_y:start_y + current_img.shape[0],
                          start_x:start_x + current_img.shape[1]] = current_img
            next_frame = frame.copy()
            start_x = int((800 - next_img.shape[1])/2)
            start_y = int((480 - next_img.shape[0])/2)
            next_frame[start_y:start_y + next_img.shape[0],
                       start_x:start_x + next_img.shape[1]] = next_img
            alpha = (x - 2500) / 500
            beta = 1.0 - alpha
            dst = cv2.addWeighted(current_frame, alpha, next_frame, beta, 0.0)
            cv2.imshow(framename, dst)
        else:
            current_frame = frame.copy()
            start_x = int((800 - current_img.shape[1])/2)
            start_y = int((480 - current_img.shape[0])/2)
            current_frame[start_y:start_y + current_img.shape[0],
                          start_x:start_x + current_img.shape[1]] = current_img
            cv2.imshow(framename, current_frame)

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
