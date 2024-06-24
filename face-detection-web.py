
import cv2
from flask import Flask, render_template, Response

def detect(cascade, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, 1.1, 6, cv2.CASCADE_SCALE_IMAGE, (50, 50))

    if len(faces) >= 1:
        scores = [0.99 for f in faces]

        # Non-maximal Suppression to remove duplicates
        # TODO: This isn't working as well as I'd like...
        indices = cv2.dnn.NMSBoxes(faces, scores, score_threshold=0.8, nms_threshold=0.2)

        for i in indices:
            x, y, w, h = faces[i]

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    return frame

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    # Load cascade
    face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

    # Find camera and start capture
    success = False
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if not cap.isOpened():
            continue
        success, frame = cap.read()
        if success:
            print("Camera ", i, " found")
            break
        else:
            cap.release()
    
    while success:
        success, frame = cap.read()
        if success:
            detect(face_cascade, frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')
    
    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
