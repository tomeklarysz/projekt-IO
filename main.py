import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from face_auth.authenticator import FaceAuthenticator
from face_auth.camera import Camera
from QR.scanner import scan_qr_code

# Dodany import do sprawdzania statusu
from database.db_operations import log_verification_event, get_latest_status

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
                scan_result = scan_qr_code(camera)
                
                if scan_result == "QUIT":
                    print("Exiting application...")
                    break
                
                if not scan_result:
                    time.sleep(1)
                    continue
                    
                user_data = scan_result
                print(f"QR Validated. Proceeding to Face Auth for User: {user_data.get('first_name')}")
                
                # Step 2: Face Authentication
                success, message = auth.verify_user(user_data, camera, timeout=10)
                
                print(f"\nAuthentication Result: {'SUCCESS' if success else 'FAILURE'}")
                print(f"Details: {message}")
                
                if success:
                    last_record = get_latest_status(user_data.get('id'))
                    is_at_work = last_record[2] if last_record else False
                    
                    if not is_at_work:
                        print("Access GRANTED.")
                        log_verification_event(user_data.get('qr_hash'), True, "Access Granted")
                    else:
                        print(f"Access DENIED. User {user_data.get('first_name')} is no longer at work.")
                        log_verification_event(user_data.get('qr_hash'), False, f"User {user_data.get('first_name')} is no longer at work")
                    
                    time.sleep(2) 
                else:
                    print("Access DENIED.")
                    log_verification_event(user_data.get('qr_hash'), False, "Access Denied")
                    time.sleep(2)

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