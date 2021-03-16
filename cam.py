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
slide_transition = 0

def bincount_app(a):
    a2D = a.reshape(-1,a.shape[-1])
    col_range = (256, 256, 256) # generically : a2D.max(0)+1
    a1D = np.ravel_multi_index(a2D.T, col_range)
    return np.unravel_index(np.bincount(a1D).argmax(), col_range)

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
background0_color = bincount_app(previous_img)
background1_color = bincount_app(current_img)
background0_overlay = np.zeros([480, 800, 3], dtype=np.uint8)
background1_overlay = np.zeros([480, 800, 3], dtype=np.uint8)
background0_overlay[:,:] = bincount_app(previous_img)
background1_overlay[:,:] = bincount_app(current_img)
matting0 = cv2.addWeighted(bg_frame.copy(), 0.50, background0_overlay.copy(), 0.50, 0)
matting1 = cv2.addWeighted(bg_frame.copy(), 0.50, background1_overlay.copy(), 0.50, 0)
slide = insert_photo(matting1.copy(), scaled_img)
cv2.imshow('Cam', slide)
while(True): 
    x += 1
    j += 1
    if x > 2000:
        x = 0
    elif x == 1:
        try:
            buffer = requests.get(url).text
            server_filenames = json.loads(str(buffer)).get('files')
            local_filenames = glob.glob(os.path.join(path, "*"))
            for s in server_filenames:
                if s not in [i.replace(local_base, "") for i in local_filenames]:
                    print(s)
                    urllib.request.urlretrieve(image_locations + s, local_base + s)
                    filenames = glob.glob(os.path.join(path, "*"))
        except:
            print("Could not load new files.")
        current_width = scaled_img.shape[1] 
        current_height = scaled_img.shape[0] 
        slide = insert_photo(matting1.copy(), scaled_img)
        #cv2.imshow('Cam', slide)
    elif x == 1800:
        previous_img = current_img.copy()
        file_index = random.randrange(0, len(filenames))
        current_img = cv2.imread(filenames[file_index])
        background0_color = bincount_app(previous_img)
        background1_color = bincount_app(current_img)
        background0_overlay = np.zeros([480, 800, 3], dtype=np.uint8)
        background1_overlay = np.zeros([480, 800, 3], dtype=np.uint8)
        background0_overlay[:,:] = bincount_app(previous_img)
        background1_overlay[:,:] = bincount_app(current_img)
        matting0 = background0_overlay.copy()
        matting1 = background1_overlay.copy()
        if current_img.shape[1] > max_width or current_img.shape[0] > max_height:
            scale = min(max_width / current_img.shape[1], max_height / current_img.shape[0])
            scaled_img = cv2.resize(current_img, (int(current_img.shape[1] * scale), int(current_img.shape[0] * scale))).copy() 
        else:
            scaled_img = current_img.copy()
    elif x > 1900:
        if x == 1901:
            slide_transition = random.randrange(0, 5)
            print(slide_transition)
        if slide_transition == 0:
            current_width -= 1
            current_height -= 1 
            fade_img = cv2.resize(previous_img, (current_width, current_height))
            slide0 = insert_photo(matting0.copy(), fade_img)
            slide1 = insert_photo(matting1.copy(), scaled_img)
            image_new = cv2.addWeighted(slide1, (x-1900)/100, slide0, 1 - (x-1900)/100, 0)
            cv2.imshow('Cam', image_new)
        elif slide_transition == 1:
            fade_img = cv2.resize(previous_img, (current_width, current_height))
            slide0 = insert_photo(matting0.copy(), fade_img)
            slide1 = insert_photo(matting1.copy(), scaled_img)
            image_new = slide0.copy()
            image_new[0:241,0:int((x-1900)/100.0*800)] = slide1[0:241:,-int((x-1900)/100.0*800):800]
            image_new[241:481,-int((x-1900)/100.0*800):800] = slide1[241:481:,0:int((x-1900)/100.0*800)]
            cv2.imshow('Cam', image_new)
        elif slide_transition == 2:
            fade_img = cv2.resize(previous_img, (current_width, current_height))
            slide0 = insert_photo(matting0.copy(), fade_img)
            slide1 = insert_photo(matting1.copy(), scaled_img)
            image_new = slide0.copy()
            image_new[0:int((x-1900)/100.0*800), 0:401] = slide1[-int((x-1900)/100.0*800):480:,0:401]
            image_new[-int((x-1900)/100.0*800):800, 400:801] = slide1[0:int((x-1900)/100.0*800), 400:801]
            cv2.imshow('Cam', image_new)
        elif slide_transition == 3:
            fade_img = cv2.resize(previous_img, (current_width, current_height))
            slide0 = insert_photo(matting0.copy(), fade_img)
            slide1 = insert_photo(matting1.copy(), scaled_img)
            image_new = slide0.copy()
            image_new[0:int((x-1900)/100.0*800), 0:267] = slide1[-int((x-1900)/100.0*800):480:,0:267]
            image_new[-int((x-1900)/100.0*800):800, 266:533] = slide1[0:int((x-1900)/100.0*800), 266:533]
            image_new[0:int((x-1900)/100.0*800), 532:800] = slide1[-int((x-1900)/100.0*800):480:,532:800]
            cv2.imshow('Cam', image_new)
        elif slide_transition ==  4:
            fade_img = cv2.resize(previous_img, (current_width, current_height))
            slide0 = insert_photo(matting0.copy(), fade_img)
            slide1 = insert_photo(matting1.copy(), scaled_img)
            i = 0
            image_new = slide0.copy()
            y1 = 230
            y2 = 250
            while i < 80:
                image_new[y1:y2, 0:i*10] = slide1[y1:y2, 0:i*10]
                cv2.imshow('Cam', image_new.copy())
                if cv2.waitKey(2) & 0xFF == ord('s'): s
                i += 1
            i = 0
            while i < 92:
                image_new[y1 - int(i/4*23):y2 + int(i/4*23), 0:800] = slide1[y1 - int(i/4*23):y2 + int(i/4*23), 0:800]
                cv2.imshow('Cam', image_new.copy())
                if cv2.waitKey(2) & 0xFF == ord('s'): s
                i += 1
                
            x = 2000
        
    if cv2.waitKey(1) & 0xFF == ord('s'): 
        break
 
                       
cv2.destroyAllWindows()
