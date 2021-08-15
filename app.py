from flask import Flask, render_template, Response
import cv2
import imutils

app = Flask(__name__)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 20)
cap.set(3, 640)
cap.set(4, 480)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
def gen_frames():
    while True:
        ret, frame = cap.read()  # read the camera frame
        image = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
        resized_image = imutils.resize(image, width=500)
        gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if firstFrame is None:
            firstFrame = gray
            continue
            
        if not ret:
            break
        else:     
            ret, buffer = cv2.imencode('.jpg', gray)
            stream_frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + stream_frame + b'\r\n')
@app.route('/')
def index():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run()
