import time
import cv2
from database.queries import get_employee_face_data, update_employee_vector
from face_auth.camera import Camera
from face_auth.recognizer import FaceRecognizer
import numpy as np

class FaceAuthenticator:
    def __init__(self):
        self.recognizer = FaceRecognizer()

    def ensure_user_has_vector(self, user_id):
        """
        Checks if the user has a face vector in the DB.
        If not, tries to generate it from the stored photo_path.
        Returns:
            (vector, error_message): (numpy_array, None) if success/exists, 
                                     (None, error_message) if failure.
        """
        user_data = get_employee_face_data(user_id)
        if not user_data:
            return None, "User not found in database."
        
        first_name, known_vector, photo_path = user_data

        print(f"Found user: {first_name}")
        
        if known_vector is not None:
            return known_vector, None
            
        # Vector is missing, try to generate from photo
        if not photo_path:
            return None, "No face data (vector or photo) found for user."
            
        # try:
        #     print(f"Generating vector from photo: {photo_path}")
        #     image = self.recognizer.load_image_file(photo_path)
        #     if image is None:
        #          return None, f"Could not load image from {photo_path}"

        #     known_vector = self.recognizer.get_face_encoding(image)
        #     if known_vector is not None:
        #         # Save it for future use
        #         update_employee_vector(user_id, known_vector)
        #         return known_vector, None
        #     else:
        #         return None, "Could not extract face features from stored photo."
        # except Exception as e:
        #     return None, f"Error processing stored photo: {e}"

    def verify_user(self, user_id, timeout=10):
        """
        Verifies if the person in front of the camera matches the user_id.
        Returns:
            (bool, str): (True/False, Message)
        """
        # 1. Ensure we have a vector to compare against
        known_vector, error = self.ensure_user_has_vector(user_id)
        if known_vector is None:
            return False, error

        # 2. Start Camera and Capture
        print("Starting camera for verification...")
        try:
            with Camera() as cam:
                start_time = time.time()
                while time.time() - start_time < timeout:
                    frame = cam.get_frame()
                    
                    # Show camera feed
                    cv2.imshow("Face Authentication", frame)
                    # Allow UI to update and check for 'q' to quit
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        return False, "User cancelled verification."

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
        finally:
            cv2.destroyAllWindows()
