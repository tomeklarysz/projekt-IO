import cv2
from database.db_operations import get_employee_by_qr
import time

def scan_qr_code(camera_instance):
    """
    Opens the camera to scan for a QR code.
    Verifies the scanned code against the database (qr_hash).
    Returns the employee dict if successful, or None/QUIT.
    """

    detector = cv2.QRCodeDetector()
    
    print("Scanning for QR code... Press 'q' to quit application.")

    while True:
        try:
            frame = camera_instance.get_frame()
        except RuntimeError as e:
            print(f"Scanner error: {e}")
            break

        data, bbox, _ = detector.detectAndDecode(frame)

        if data:
            print(f"QR Code detected: {data}")
            # checking against qr_hash
            # checking against qr_hash
            employee = get_employee_by_qr(data)
            if employee:
                print(f"SUCCESS: User '{employee['first_name']}' found via QR.")
                
                # Visual Feedback: Draw success message
                # Bounding box is optional, but we can draw text
                cv2.putText(frame, f"QR ACCEPTED: {employee['first_name']}", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Access Control", frame)
                cv2.waitKey(1000) # Show for 1 second

                return employee # Return the full user dict
            else:
                print("PERMISSION DENIED: QR code not recognized.")
                # Prevent spamming the message
                time.sleep(2)

        cv2.imshow("Access Control", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quit signal received in scanner.")
            # Signal to stop the whole app
            return "QUIT"
            
    return None
