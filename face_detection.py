
import cv2

class FaceDetection:
    def __init__(self):
        self.cap = cv2.VideoCapture()
        self.face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
        self.camera_started = False

    def start_camera(self):
        if self.cap.isOpened() or self.camera_started:
            return

        success = False
        for i in range(5):
            if not self.cap.open(i):
                continue

            success, frame = self.cap.read()
            if success:
                print("Camera ", i, " found")
                break
            else:
                self.cap.release()

        if not success:
            print("No camera found")

    def stop_camera(self):
        self.cap.release()

    def get_frame(self):
        if not self.cap.isOpened():
            return False, None
        return self.cap.read()

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 6, cv2.CASCADE_SCALE_IMAGE, (50, 50))

        if len(faces) >= 1:
            scores = [0.99 for f in faces]

            # Non-maximal Suppression to remove duplicates
            # TODO: This isn't working as well as I'd like...
            indices = cv2.dnn.NMSBoxes(faces, scores, score_threshold=0.8, nms_threshold=0.2)
            
            for i in indices:
                x, y, w, h = faces[i]

                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        return frame


if __name__ == "__main__":
    # Starting window
    start_img = cv2.imread("images/PR_camera_search.png")
    cv2.imshow("Face Detection", start_img)
    cv2.waitKey(1000)

    fdetect = FaceDetection()
    fdetect.start_camera()

    while True:
        success, frame = fdetect.get_frame()

        if success:
            fdetect.detect(frame)
            cv2.imshow("Face Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    fdetect.stop_camera()
    cv2.destroyAllWindows()
