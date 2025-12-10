import time
import cv2
from database.queries import update_employee_vector
from face_auth.recognizer import FaceRecognizer
import numpy as np

class FaceAuthenticator:
    def __init__(self):
        self.recognizer = FaceRecognizer()

    def ensure_user_has_vector(self, user_data):
        """
        Checks if the user has a face vector in the DB (passed via user_data).
        If not, tries to generate it from the stored photo_path.
        Returns:
            (vector, error_message): (numpy_array, None) if success/exists, 
                                     (None, error_message) if failure.
        """
        if not user_data:
             return None, "No user data provided."

        user_id = user_data['id']
        first_name = user_data['first_name']
        known_vector = user_data['vector_features']
        photo_path = user_data['photo_path']

        print(f"Verifying user: {first_name} (ID: {user_id})")
        
        if known_vector is not None:
            # When coming from DB, it might be a list or numpy array
            if isinstance(known_vector, list):
                return np.array(known_vector), None
            return known_vector, None
            
        # Vector is missing, try to generate from photo
        if not photo_path:
            return None, "No face data (vector or photo) found for user."
            
        try:
            print(f"Generating vector from photo: {photo_path}")
            image = self.recognizer.load_image_file(photo_path)
            if image is None:
                 return None, f"Could not load image from {photo_path}"

            known_vector = self.recognizer.get_face_encoding(image)
            if known_vector is not None:
                # Save it for future use
                update_employee_vector(user_id, known_vector)
                return known_vector, None
            else:
                return None, "Could not extract face features from stored photo."
        except Exception as e:
            return None, f"Error processing stored photo: {e}"

    def verify_user(self, user_data, camera_instance, timeout=10):
        """
        Verifies if the person in front of the camera matches the user described in user_data.
        Returns:
            (bool, str): (True/False, Message)
        """
        # 1. Ensure we have a vector to compare against
        known_vector, error = self.ensure_user_has_vector(user_data)
        if known_vector is None:
            return False, error

        # 2. Start Camera and Capture
        print(f"Starting verification for User: {user_data.get('first_name', 'Unknown')}...")
        try:
            # We use the existing camera_instance
            window_name = "Face Authentication"
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    frame = camera_instance.get_frame()
                except RuntimeError as e:
                    return False, f"Camera error during verification: {e}"
                
                # Show camera feed
                cv2.imshow(window_name, frame)
                # Allow UI to update and check for 'q' to quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return False, "User cancelled verification."

                # Try to get encoding from current frame
                unknown_vector = self.recognizer.get_face_encoding(frame)
                
                if unknown_vector is not None:
                    # 3. Compare
                    match = self.recognizer.compare_faces(known_vector, unknown_vector)
                    if match:
                        cv2.destroyWindow(window_name)
                        return True, "Verification successful."
                    else:
                        print("Face detected but not matching...")
                
                time.sleep(0.1)
            
            cv2.destroyWindow(window_name)
            return False, "Verification timed out. Face not matched."
        except Exception as e:
            return False, f"Error during verification: {e}"

