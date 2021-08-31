import cv2

cap = cv2.VideoCapture(0)
framename = "WatchThis"
cv2.namedWindow(framename, cv2.WINDOW_FREERATIO)
frame = cv2.imread("frame.jpg")
cv2.imshow(framename, frame)
max_width = 700
max_height = 480


while True:
    success, frame = cap.read()
    image = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
    image = cv2.flip(image, 1)
    scale = min(max_width / image.shape[1], max_height / image.shape[0])
    current_img = cv2.resize(image, (int(image.shape[1] * scale), int(image.shape[0] * scale)))
    current_frame = frame.copy()
    start_x = int((800 - current_img.shape[1])/2)
    start_y = int((480 - current_img.shape[0])/2)
    current_frame[start_y:start_y + current_img.shape[0],
                  start_x:start_x + current_img.shape[1]] = current_img
    cv2.imshow(framename, current_frame)
    
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        cv2.destroyAllWindows()
        break
