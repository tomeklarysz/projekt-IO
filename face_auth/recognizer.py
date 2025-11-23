import face_recognition
import numpy as np
import cv2

class FaceRecognizer:
    def get_face_encoding(self, image):
        """
        Computes the 128-d face encoding for the first face in the image.
        Returns None if no face is found.
        """
        # Convert BGR (OpenCV) to RGB (face_recognition)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detect face locations first to speed up encoding
        face_locations = face_recognition.face_locations(rgb_image)
        if not face_locations:
            return None
            
        # Compute encodings (we only take the first one for 1:1 auth)
        encodings = face_recognition.face_encodings(rgb_image, face_locations)
        if encodings:
            return encodings[0]
        return None

    def compare_faces(self, known_vector, unknown_vector, tolerance=0.6):
        """
        Compares a known face vector with an unknown face vector.
        Returns True if they match, False otherwise.
        """
        if known_vector is None or unknown_vector is None:
            return False
            
        # face_recognition.compare_faces returns a list of True/False
        # We compare one against one
        results = face_recognition.compare_faces([np.array(known_vector)], np.array(unknown_vector), tolerance=tolerance)
        return results[0]

    def load_image_file(self, path):
        """Loads an image file."""
        return face_recognition.load_image_file(path)
