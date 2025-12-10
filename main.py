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
                # This will block until a valid QR is found or 'QUIT' is returned
                qr_data = scan_qr_code(camera)
                
                if qr_data == "QUIT":
                    print("Exiting application...")
                    break
                
                if not qr_data:
                    # Scanner returned None likely due to error, retry loop
                    time.sleep(1)
                    continue
                    
                try:
                    user_id = int(qr_data) # Assuming QR data is just the ID
                except ValueError:
                    print(f"Error: Scanned QR data '{qr_data}' is not a valid numeric User ID.")
                    time.sleep(2)
                    continue

                print(f"QR Validated. Proceeding to Face Auth for User ID: {user_id}")
                
                # Step 2: Face Authentication
                # We pass the same camera instance
                success, message = auth.verify_user(user_id, camera, timeout=10)
                
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

if __name__ == "__main__":
    main()
