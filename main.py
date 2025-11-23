import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from face_auth.authenticator import FaceAuthenticator

def main():
    print("--- Face Authentication System ---")
    try:
        user_input = input("Enter User ID to verify (or 'q' to quit): ")
        if user_input.lower() == 'q':
            return
        
        user_id = int(user_input)
    except ValueError:
        print("Invalid ID format. Please enter a numeric ID.")
        return

    print(f"Initializing authentication for User ID: {user_id}...")
    
    auth = FaceAuthenticator()
    
    # verify_user will automatically check for vector features and
    # generate them if missing via the ensure_user_has_vector method
    success, message = auth.verify_user(user_id)
    
    print("\n--- Result ---")
    print(f"Status: {'SUCCESS' if success else 'FAILURE'}")
    print(f"Message: {message}")
    print("----------------")

if __name__ == "__main__":
    main()
