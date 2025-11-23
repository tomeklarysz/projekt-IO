import os
from face_auth.recognizer import FaceRecognizer
from database.queries import upsert_employee_vector

def upsert_employee_from_photo(photo_path, employee_id, first_name=None, last_name=None, qr_hash=None):
    """
    Updates or inserts an employee's face vector using a provided photo.
    
    Args:
        photo_path (str): Path to the photo file.
        employee_id (int): ID of the employee.
        first_name (str, optional): First name (required for new employee).
        last_name (str, optional): Last name (required for new employee).
        qr_hash (str, optional): QR Hash (required for new employee).
        
    Returns:
        str: Result message ("Updated", "Created", "Not Found", "Error", or specific error details).
    """
    if not os.path.exists(photo_path):
        return f"Error: Photo file not found at {photo_path}"
        
    try:
        recognizer = FaceRecognizer()
    except Exception as e:
        return f"Error initializing FaceRecognizer: {e}"
        
    image = recognizer.load_image_file(photo_path)
    if image is None:
        return "Error: Could not load image."
        
    embedding = recognizer.get_face_encoding(image)
    
    if embedding is None:
        return "Error: No face found in the image or could not extract features."
        
    result = upsert_employee_vector(
        employee_id, 
        embedding, 
        first_name=first_name, 
        last_name=last_name, 
        qr_hash=qr_hash,
        photo_path=photo_path
    )
    
    return result
