import cv2

cap = cv2.VideoCapture(0)
framename = "WatchThis"
cv2.namedWindow(framename, cv2.WINDOW_FREERATIO)
frame = cv2.imread("frame.jpg")
cv2.imshow(framename, frame)
max_width = 600
max_height = 300


while True:
    success, frame = cap.read()
    image = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
    image = cv2.flip(image, 1)
    scale = min(max_width / image.shape[1], max_height / image.shape[0])
    current_img = cv2.resize(image, (int(image.shape[1] * scale), int(image.shape[0] * scale)))
    cv2.imshow(framename, current_img)
    
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        cv2.destroyAllWindows()
        break
