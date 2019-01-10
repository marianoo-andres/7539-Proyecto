import face_recognition


class FaceEncoder():
    def encode(self, image, face_locations):
        """
        PRE: There is a face in the image
        """
        # Encode the face
        face_encodings = face_recognition.face_encodings(image, face_locations)
        return face_encodings