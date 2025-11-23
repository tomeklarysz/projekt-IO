import time
from database.queries import get_employee_face_data, update_employee_vector
from face_auth.camera import Camera
from face_auth.recognizer import FaceRecognizer
import numpy as np

class FaceAuthenticator:
    def __init__(self):
        self.recognizer = FaceRecognizer()

    def verify_user(self, user_id, timeout=10):
        """
        Verifies if the person in front of the camera matches the user_id.
        Returns:
            (bool, str): (True/False, Message)
        """
        # 1. Fetch user data
        user_data = get_employee_face_data(user_id)
        if not user_data:
            return False, "User not found in database."
        
        known_vector, photo_path = user_data
        
        # If we don't have a vector but have a photo, compute vector now
        if known_vector is None:
            if photo_path:
                try:
                    image = self.recognizer.load_image_file(photo_path)
                    known_vector = self.recognizer.get_face_encoding(image)
                    if known_vector is not None:
                        # Save it for future use
                        update_employee_vector(user_id, known_vector)
                    else:
                        return False, "Could not extract face features from stored photo."
                except Exception as e:
                    return False, f"Error loading stored photo: {e}"
            else:
                return False, "No face data (vector or photo) found for user."

        # 2. Start Camera and Capture
        print("Starting camera for verification...")
        try:
            with Camera() as cam:
                start_time = time.time()
                while time.time() - start_time < timeout:
                    frame = cam.get_frame()
                    
                    # Try to get encoding from current frame
                    unknown_vector = self.recognizer.get_face_encoding(frame)
                    
                    if unknown_vector is not None:
                        # 3. Compare
                        match = self.recognizer.compare_faces(known_vector, unknown_vector)
                        if match:
                            return True, "Verification successful."
                        else:
                            # We found a face but it didn't match. 
                            # We could return immediately or keep trying until timeout.
                            # Let's keep trying for a bit in case of bad angle, but maybe not full timeout if we want fast fail.
                            # For now, let's just print and continue
                            print("Face detected but not matching...")
                    
                    # Small sleep to not burn CPU
                    time.sleep(0.1)
                
                return False, "Verification timed out. Face not matched."
        except Exception as e:
            return False, f"Camera error: {e}"
