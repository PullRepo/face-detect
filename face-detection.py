
import cv2
import numpy as np

px, py, pw, ph = (0, 0, 0, 0)

def detect(cascade, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, 1.1, 6, cv2.CASCADE_SCALE_IMAGE, (50, 50))

    if len(faces) >= 1:
        scores = [0.99 for f in faces]

        # Non-maximal Suppression to remove duplicates
        # TODO: This isn't working as well as I'd like...
        indices = cv2.dnn.NMSBoxes(faces, scores, score_threshold=0.8, nms_threshold=0.2)

        global px
        global py
        global pw
        global ph
        px, py, pw, ph = faces[0]
        for i in indices:
            x, y, w, h = faces[i]

            alpha = 0.6
            beta = 1.0 - alpha

            # Smooth the rectangle over time
            # TODO: This also isn't working as well as I'd like...
            X = round(alpha * x + beta * px)
            Y = round(alpha * y + beta * py)
            W = round(alpha * w + beta * pw)
            H = round(alpha * h + beta * ph)

            cv2.rectangle(frame, (X, Y), (X+W, Y+H), (255, 0, 0), 2)

            px, py, pw, ph = (x, y, w, h)

    return frame

def display(frame):
    cv2.imshow("Face Detection", frame)

if __name__ == "__main__":

    # Starting window
    start_img = cv2.imread("images/PR_camera_search.png")
    (h, w, c) = start_img.shape[:3]
    cv2.imshow("Face Detection", start_img)
    cv2.waitKey(1000)

    # Load cascade
    face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

    success = False

    # Start Video Capture
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

    if not success:
        err_img = cv2.imread("images/PR_camera_unk.png")
        cv2.imshow("Face Detection", err_img)
        cv2.waitKey(3000)
        cv2.destroyAllWindows()
        exit(-1)

    while success:
        success, frame = cap.read()
        if success:
            detect(face_cascade, frame)
            display(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
