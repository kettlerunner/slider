import cv2

cap = cv2.VideoCapture(0)
framename = "WatchThis"
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
max_width = 600
max_height = 400


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
        image = image[ty:ty+300, tx:bx]
        faces = faces[np.argmax(face_sizes):np.argmax(face_sizes)+1]
    else:
        tx = int(img.shape[1]/2 - 150)
        ty = int(img.shape[0]/2 - 150)
        image = image[ty:ty+300, tx:tx+300]
        
    scale = min(max_width / image.shape[1], max_height / image.shape[0])
    current_img = cv2.resize(image, (int(image.shape[1] * scale), int(image.shape[0] * scale)))
    cv2.imshow(framename, current_img)
    
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        cv2.destroyAllWindows()
        break
