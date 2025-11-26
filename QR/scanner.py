import cv2
import database
import time

def scan_qr_code():
    """
    Opens the camera to scan for a QR code.
    Verifies the scanned code against the database.
    """
    # Ensure database is initialized (just in case)
    database.init_db()

    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    detector = cv2.QRCodeDetector()
    
    print("Scanning for QR code... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        data, bbox, _ = detector.detectAndDecode(frame)

        if data:
            print(f"QR Code detected: {data}")
            if database.verify_code(data):
                print("SUCCESS: QR code recognized and verified in database.")
                # Optional: Wait a bit or break immediately
                # time.sleep(2) 
                break
            else:
                print("PERMISSION DENIED: QR code not recognized.")
                # Prevent spamming the message
                time.sleep(2)

        cv2.imshow("QR Code Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
