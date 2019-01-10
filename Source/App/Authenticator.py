from Camera import Camera
from FaceDetector import FaceDetector
from FaceEncoder import FaceEncoder
from FaceIdentificator import FaceIdentificator
from Person import Person
import os
import time
class Authenticator:
    def __init__(self):
        self.init()
        self.setPersons()
    def init(self):
        self.faceDetector = FaceDetector()
        self.faceEncoder = FaceEncoder()
        self.camera = Camera()

        self.faceImageArray = None
        self.faceEncoding = None  

        self.personAuthenticated = None

    def setPersons(self):
        self.persons = []
        for fileName in os.listdir("Database"):
            if fileName == '.DS_Store':
                continue
            self.persons.append(Person(dirName = fileName))

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
        self.faceIdentificator = FaceIdentificator(self.persons, self.faceEncoding)
        return True

    def getPersonFaceAuthenticated(self):
        return self.faceIdentificator.getPersonFaceAuthenticated()

    def authenticateFace(self):
        faceDetected = self.setFace()
        if not faceDetected:
            return None
        person = self.getPersonFaceAuthenticated()
        self.personAuthenticated = person
        return person # if no face authenticated person is "Unknown"
    def authenticate(self, data):
        personDNI = Person(data)
        return self.personAuthenticated.same(personDNI)

       