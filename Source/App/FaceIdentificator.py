import face_recognition
import numpy as np
class FaceIdentificator:
	def __init__(self, persons, faceEncoding):
		self.persons = persons
		self.faceEncoding = faceEncoding

	def getPersonFaceAuthenticated(self):
		known_face_encodings = [ person.encoding for person in self.persons ]
		# Calculate distances of face to known faces
		distances = face_recognition.face_distance(known_face_encodings, self.faceEncoding)

		# Get the index and min distance
		min_distance_index = np.argmin(distances)
		min_distance = distances[min_distance_index]
		threshold = 0.6  # Recommended value

		# Get the name
		if min_distance < threshold:
		    personAuthenticated = self.persons[min_distance_index]
		else:
		    personAuthenticated = "Unknown"
		return personAuthenticated