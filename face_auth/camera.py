import cv2
import time

class Camera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None

    def start(self):
        """Starts the camera capture."""
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open camera with index {self.camera_index}")
        # Allow camera to warm up
        time.sleep(1.0)

    def get_frame(self):
        """Captures a single frame from the camera."""
        if not self.cap or not self.cap.isOpened():
            raise RuntimeError("Camera is not started. Call start() first.")
        
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to capture frame from camera.")
        return frame

    def stop(self):
        """Releases the camera."""
        if self.cap:
            self.cap.release()
            self.cap = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
