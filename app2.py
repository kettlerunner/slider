import cv2
import numpy as np

cap = cv2.VideoCapture(0)
framename = "WatchThis"
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
max_width = 300
max_height = 300


while True:
    success, frame = cap.read()
    image = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
    image = cv2.flip(image, 1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)
    face_sizes = []
    face_images = []
    for (x, y, w, h) in faces:
        face_sizes.append(w*h)
        cv2.rectangle(image, (x-5, y-5), (x+w+5, y+h+5), (255, 255, 255), 2)
    
    if len(face_sizes) > 0:
        (x, y, w, h) = faces[np.argmax(face_sizes)]
        tx = int(x+w/2-150)
        ty = int(y+h/2-150)
        if tx < 0: tx = 0
        if ty < 0: ty = 0
        bx = tx + 300
        by = ty + 300
        if bx > 480:
            tx = tx - (bx-480)
            bx = tx + 300
        face_image = image[y:y+h, x:x+w]
        image = image[ty:ty+300, tx:bx]
        cv2.imshow(framename, face_image)
        faces = faces[np.argmax(face_sizes):np.argmax(face_sizes)+1]
    else:
        tx = int(image.shape[1]/2 - 150)
        ty = int(image.shape[0]/2 - 150)
        image = image[ty:ty+300, tx:tx+300]
        cv2.imshow(framename, image)
    
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        cv2.destroyAllWindows()
        break
