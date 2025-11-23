import sys
import os

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
        # Note: You need a real photo path for this to work fully, 
        # or we can manually insert a vector if we had one.
        # For now, we'll insert a placeholder and expect the user to provide a valid path or vector manually for a real test.
        cur.execute("""
            INSERT INTO employees (first_name, last_name, qr_hash, photo_path)
            VALUES ('Test', 'User', 'test_qr_hash', 'photos/scan.jpg')
            RETURNING id
        """)
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
