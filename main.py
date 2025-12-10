import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from face_auth.authenticator import FaceAuthenticator
from face_auth.camera import Camera
from QR.scanner import scan_qr_code

def main():
    print("--- Access Control System ---")
    print("Initializing Camera...")
    
    try:
        with Camera() as camera:
            # Initialize authenticator once
            auth = FaceAuthenticator()
            
            while True:
                print("\n--- READY For Next User ---")
                
                # Step 1: Scan QR Code
                # This will block until a valid QR is found (returning user dict) or 'QUIT' is returned
                scan_result = scan_qr_code(camera)
                
                if scan_result == "QUIT":
                    print("Exiting application...")
                    break
                
                if not scan_result:
                    # Scanner returned None likely due to error, retry loop
                    time.sleep(1)
                    continue
                    
                user_data = scan_result
                print(f"QR Validated. Proceeding to Face Auth for User: {user_data.get('first_name')}")
                
                # Step 2: Face Authentication
                # We pass the same camera instance and the user data
                success, message = auth.verify_user(user_data, camera, timeout=10)
                
                print(f"\nAuthentication Result: {'SUCCESS' if success else 'FAILURE'}")
                print(f"Details: {message}")
                
                if success:
                    print("Access GRANTED.")
                    time.sleep(2) # Show success message for a bit
                else:
                    print("Access DENIED.")
                    time.sleep(2) # Show failure message for a bit

    except Exception as e:
        print(f"Critical System Error: {e}")
    finally:
        print("System shutdown.")
        try:
            import cv2
            cv2.destroyAllWindows()
        except:
            pass

if __name__ == "__main__":
    main()
