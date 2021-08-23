from flask import Flask, render_template, Response
import cv2
import numpy as np

app = Flask(__name__)

net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
classes = []
with open('coco.names', 'r') as f:
    classes = f.read().splitlines()
cap = cv2.VideoCapture(0)
cv2.namedWindow('Cam', cv2.WINDOW_AUTOSIZE)
cap.set(cv2.CAP_PROP_FPS, 20)
cap.set(3, 640)
cap.set(4, 480)
fourcc = cv2.VideoWriter_fourcc(*'XVID')


def gen_frames():
    while True:
        ret, frame = cap.read()  # read the camera frame
        image = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
        image = cv2.flip(image, 1)
        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 1/255, (219,219), (0,0,0), swapRB=True, crop=False)
        net.setInput(blob)
        output_layers_names = net.getUnconnectedOutLayersNames()
        layerOutputs = net.forward(output_layers_names)

        boxes = []
        confidences = []
        class_ids = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0]*width)
                    center_y = int(detection[1]*height)
                    w = int(detection[2]*width)
                    h = int(detection[3]*height)

                    x = int(center_x - w/2)
                    y = int(center_y - h/2)

                    boxes.append([x, y, w, h])
                    confidences.append((float(confidence)))
                    class_ids.append(class_id)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        font = cv2.FONT_HERSHEY_PLAIN
        colors = np.random.uniform(0, 255, size=(len(boxes), 3))

        if type(indexes) != tuple:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = str(round(confidences[i], 2))
                color = colors[i]
                if label == 'person':
                    cv2.rectangle(image, (x,y), (x+w, y+h), color, 2)
                    cv2.putText(image, label + " " + confidence, (x, y+20), font, 2, (255,255,255), 2)
                
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', image)
            stream_frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + stream_frame + b'\r\n')


@app.route('/')
def index():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run()

