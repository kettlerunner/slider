import cv2

cap = cv2.VideoCapture(0)


while True:
    success, frame = cap.read()
    image = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
    image = cv2.flip(image, 1)
    cv2.imshow("Video", image)
    
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        cv2.destroyAllWindows()
        break
