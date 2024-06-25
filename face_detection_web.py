
from re import T
import cv2
from face_detection import FaceDetection
from flask import Flask, render_template, Response

fdetect = FaceDetection()

def gen():
    print("Starting camera")
    fdetect.start_camera()

    success = True
    while success:
        success, frame = fdetect.get_frame()
        if success:
            fdetect.detect(frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    print("Stopping camera")
    fdetect.stop_camera()
