import cv2
from QR import database
import time

def scan_qr_code(camera_instance):
    """
    Opens the camera to scan for a QR code.
    Verifies the scanned code against the database.
    """
    database.init_db()
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
            if database.verify_code(data):
                print("SUCCESS: QR code recognized and verified in database.")
                return data
            else:
                print("PERMISSION DENIED: QR code not recognized.")
                # Prevent spamming the message
                time.sleep(2)

        cv2.imshow("QR Code Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quit signal received in scanner.")
            # Signal to stop the whole app
            return "QUIT"
            
    return None
