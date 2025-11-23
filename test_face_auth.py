import sys
import os

# Path to the photo of the test user
PHOTO_PATH = 'photos/scan.jpg'

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from face_auth.authenticator import FaceAuthenticator
from database.db_setup import get_db_connection

def setup_test_user():
    """Inserts a test user into the database if not exists."""
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to DB.")
        return None
    
    try:
        cur = conn.cursor()
        # Check if user exists
        cur.execute("SELECT id FROM employees WHERE first_name = 'Test' AND last_name = 'User'")
        res = cur.fetchone()
        if res:
            print(f"Test user already exists with ID {res[0]}")
            return res[0]
        
        # Insert test user
        # We need to compute the vector for the test user
        from face_auth.recognizer import FaceRecognizer
        recognizer = FaceRecognizer()
        
        image_path = PHOTO_PATH
        if not os.path.exists(image_path):
             print(f"Warning: Test photo {image_path} not found.")
             vector = None
        else:
            image = recognizer.load_image_file(image_path)
            vector = recognizer.get_face_encoding(image)
            
        if vector is None:
            print("Warning: Could not generate vector for test user.")
            
        # Convert vector to list for DB insertion if needed, or keep as is if DB adapter handles it.
        # Assuming DB expects a list or array.
        vector_list = vector.tolist() if hasattr(vector, 'tolist') else vector

        cur.execute("""
            INSERT INTO employees (first_name, last_name, qr_hash, vector_features, photo_path)
            VALUES ('Test', 'User', 'test_qr_hash', %s, %s)
            RETURNING id
        """, (vector_list, image_path))
        user_id = cur.fetchone()[0]
        conn.commit()
        print(f"Created test user with ID {user_id}")
        return user_id
    except Exception as e:
        print(f"Error setting up test user: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def main():
    user_id = setup_test_user()
    if not user_id:
        return

    print(f"Testing authentication for User ID: {user_id}")
    print("Please look at the camera...")
    
    auth = FaceAuthenticator()
    success, message = auth.verify_user(user_id)
    
    print(f"Result: {success}")
    print(f"Message: {message}")

if __name__ == "__main__":
    main()
