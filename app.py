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
    firstFrame = None
    
    while True:
        ret, frame = cap.read()  # read the camera frame
        image = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
        image = cv2.flip(image, 1)
        resized_image = imutils.resize(image, width=500)
        gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if firstFrame is None:
            firstFrame = gray
            continue
            
        frameDelta = cv2.absdiff(firstFrame, gray)
	    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
	    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	    cnts = imutils.grab_contours(cnts)

        for c in cnts:
            if cv2.contourArea(c) < args["min_area"]:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"
       
        cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.imshow("Security Feed", frame)
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frameDelta)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            cv2.destroyAllWindows()
		    break
            
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
