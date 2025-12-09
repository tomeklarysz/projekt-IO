import face_recognition
import numpy as np
import cv2

class FaceRecognizer:
    def __init__(self):
        print("FaceRecognizer initialized using face_recognition library.")

    def get_face_encoding(self, image):
        """
        Computes the face embedding for the first face in the image.
        Returns None if no face is found.
        Args:
            image: numpy array (BGR or RGB).
        """
        try:
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            encodings = face_recognition.face_encodings(rgb_image)
            
            if not encodings:
                return None
                
            return encodings[0]
            
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None

    def compare_faces(self, known_vector, unknown_vector, threshold=0.6):
        """
        Compares a known face vector with an unknown face vector.
        Uses Euclidean distance (face_recognition default).
        Returns True if distance < threshold.
        Default threshold for face_recognition is 0.6.
        """
        if known_vector is None or unknown_vector is None:
            return False
            
        v1 = np.array(known_vector)
        v2 = np.array(unknown_vector)
        
        # face_recognition.face_distance returns a list of distances
        # We pass [v1] as known_faces and v2 as face_to_compare
        # But v2 is a single encoding, face_distance expects face_to_compare to be the encoding itself (not a list)
        
        distances = face_recognition.face_distance([v1], v2)
        distance = distances[0]
        
        return distance < threshold

    def load_image_file(self, path):
        """Loads an image file using OpenCV (returns BGR)."""
        return cv2.imread(path)
