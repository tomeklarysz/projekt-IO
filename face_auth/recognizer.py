from deepface import DeepFace
import numpy as np
import cv2

class FaceRecognizer:
    def __init__(self, model_name="Facenet"):
        self.model_name = model_name
        # Trigger a dummy call to load the model into memory
        try:
            # We use a dummy image (black square) to initialize
            dummy = np.zeros((224, 224, 3), dtype=np.uint8)
            DeepFace.represent(dummy, model_name=self.model_name, enforce_detection=False)
            print(f"DeepFace model {self.model_name} loaded.")
        except Exception as e:
            print(f"Warning: Could not initialize DeepFace model: {e}")

    def get_face_encoding(self, image):
        """
        Computes the face embedding for the first face in the image.
        Returns None if no face is found.
        """
        try:
            # DeepFace expects RGB usually, but OpenCV is BGR.
            # DeepFace.represent handles numpy arrays.
            # We'll convert to RGB to be safe/standard.
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # enforce_detection=True ensures we only get a vector if a face is actually found.
            # If False, it returns a vector for the whole image if no face is found (bad for auth).
            # However, enforce_detection=True raises an exception if no face is found.
            results = DeepFace.represent(
                img_path=rgb_image,
                model_name=self.model_name,
                enforce_detection=True,
                detector_backend='opencv' # Use opencv or retinaface (slower but better)
            )
            
            if not results:
                return None
                
            # Return the embedding of the first face found
            return results[0]["embedding"]
            
        except ValueError:
            # DeepFace raises ValueError if enforce_detection=True and no face is found
            return None
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None

    def compare_faces(self, known_vector, unknown_vector, threshold=0.4):
        """
        Compares a known face vector with an unknown face vector using Cosine Similarity.
        Returns True if distance < threshold.
        Note: For Cosine Distance, lower is better (0 = same, 1 = opposite).
        Facenet threshold is typically around 0.4.
        """
        if known_vector is None or unknown_vector is None:
            return False
            
        # Ensure numpy arrays
        v1 = np.array(known_vector)
        v2 = np.array(unknown_vector)
        
        # Compute Cosine Distance
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        
        if norm_v1 == 0 or norm_v2 == 0:
            return False
            
        cosine_similarity = dot_product / (norm_v1 * norm_v2)
        cosine_distance = 1 - cosine_similarity
        
        return cosine_distance < threshold

    def load_image_file(self, path):
        """Loads an image file using OpenCV (returns BGR)."""
        # DeepFace can read paths too, but our interface expects an image array often
        return cv2.imread(path)
