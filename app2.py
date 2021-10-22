import cv2

cap = cv2.VideoCapture(0)
framename = "WatchThis"
max_width = 600
max_height = 400


while True:
    success, frame = cap.read()
    image = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
    image = cv2.flip(image, 1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)
    face_sizes = []
    for (x, y, w, h) in faces:
        face_sizes.append(w*h)
        cv2.rectangle(image, (x-5, y-5), (x+w+5, y+h+5), (255, 255, 255), 2)
        
    scale = min(max_width / image.shape[1], max_height / image.shape[0])
    current_img = cv2.resize(image, (int(image.shape[1] * scale), int(image.shape[0] * scale)))
    cv2.imshow(framename, current_img)
    
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        cv2.destroyAllWindows()
        break
