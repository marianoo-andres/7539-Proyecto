from Camera import Camera
from FaceDetector import FaceDetector
from FaceEncoder import FaceEncoder
from Person import Person
import time
class Enroller:
    def __init__(self):
        self.init()
    def init(self):
        self.faceDetector = FaceDetector()
        self.faceEncoder = FaceEncoder()
        self.camera = Camera()

        self.faceImageArray = None
        self.faceEncoding = None   
    def setFace(self):
        # Start recording
        self.camera.start()
        face_locations = []
        startTime = time.time()
        maxWaitInSeconds = 5
        while len(face_locations) == 0:
            waitTime = time.time() - startTime
            if waitTime > maxWaitInSeconds:
                self.camera.stop()
                return False
            frame = self.camera.takePicture()
            # Detect faces
            face_locations = self.faceDetector.detect(frame, resize=True, resizeProportion=1)
            if (len(face_locations) > 0):
                face_encodings = self.faceEncoder.encode(frame, face_locations)
        self.camera.stop()

        self.faceImageArray = frame
        self.faceEncoding = face_encodings[0]
        return True

    def enroll(self, dniDataString):
        person = Person(dniDataString, self.faceImageArray, self.faceEncoding)
        person.save()
       