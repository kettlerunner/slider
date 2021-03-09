from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
cap = cv2.VideoCapture(-1)
cap.set(cv2.CAP_PROP_FPS, 20)
cap.set(3, 640)
cap.set(4, 480)
fourcc = cv2.VideoWriter_fourcc(*'XVID')


def gen_frames():
    while True:
        ret, frame = cap.read()  # read the camera frame
        if not ret:
            break
        else:     
            ret, buffer = cv2.imencode('.jpg', frame)
            stream_frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + stream_frame + b'\r\n')


@app.route('/')
def index():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(port=5001)
