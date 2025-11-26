import cv2
import database
import time

def remove_qr_code():
    """
    Opens the camera to scan for a QR code.
    If the code exists in the database, it will be removed.
    """
    # Ensure database is initialized
    database.init_db()

    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    detector = cv2.QRCodeDetector()
    
    print("Scanning for QR code to remove... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        data, bbox, _ = detector.detectAndDecode(frame)

        if data:
            print(f"QR Code detected: {data}")
            if database.verify_code(data):
                if database.delete_code(data):
                    print("SUCCESS: QR code removed from database.")
                else:
                    print("ERROR: Failed to remove QR code from database.")
                break
            else:
                print("QR code not found in database. Nothing to remove.")
                time.sleep(2)

        cv2.imshow("QR Code Remover", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
