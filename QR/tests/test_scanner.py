import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Adjust path to import scanner module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scanner

class TestScanner(unittest.TestCase):
    
    @patch('scanner.cv2.VideoCapture')
    @patch('scanner.cv2.QRCodeDetector')
    @patch('scanner.database.init_db')
    @patch('scanner.database.verify_code')
    @patch('scanner.cv2.imshow')
    @patch('scanner.cv2.waitKey')
    @patch('scanner.cv2.destroyAllWindows')
    def test_scan_qr_code_found(self, mock_destroy, mock_wait, mock_imshow, mock_verify, mock_init, mock_detector_cls, mock_video_capture):
        # Setup mocks
        mock_cap = MagicMock()
        mock_video_capture.return_value = mock_cap
        mock_cap.isOpened.return_value = True
        # First read returns (True, frame), second read we can stop or simple let logic break
        mock_cap.read.return_value = (True, "fake_frame")
        
        mock_detector = MagicMock()
        mock_detector_cls.return_value = mock_detector
        # Simulate detecting a code "test-code"
        mock_detector.detectAndDecode.return_value = ("test-code", "bbox", "rectified_image")
        
        mock_verify.return_value = True # Code exists in DB
        
        # NOTE: The loop in scanner.py is infinite until 'q' or recognizing a code. 
        # The logic has `break` when verification is successful.
        
        # Execute
        scanner.scan_qr_code()
        
        # Assertions
        mock_init.assert_called_once()
        mock_video_capture.assert_called_once_with(0)
        mock_cap.isOpened.assert_called_once()
        mock_detector.detectAndDecode.assert_called_with("fake_frame")
        mock_verify.assert_called_with("test-code")
        mock_cap.release.assert_called_once()
        mock_destroy.assert_called_once()

    @patch('scanner.cv2.VideoCapture')
    @patch('scanner.cv2.QRCodeDetector')
    @patch('scanner.database.init_db')
    @patch('scanner.database.verify_code')
    @patch('scanner.cv2.imshow')
    @patch('scanner.cv2.waitKey')
    @patch('scanner.cv2.destroyAllWindows')
    def test_scan_qr_code_not_found_then_quit(self, mock_destroy, mock_wait, mock_imshow, mock_verify, mock_init, mock_detector_cls, mock_video_capture):
        # Mock setup
        mock_cap = MagicMock()
        mock_video_capture.return_value = mock_cap
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, "fake_frame")
        
        mock_detector = MagicMock()
        mock_detector_cls.return_value = mock_detector
        
        # 1st iteration: Detect code, verify (False), then user presses 'q'
        # detectAndDecode called in loop. 
        # We need to control the loop.
        # Side effect for detectAndDecode: first return invalid code, second... wait loop control via waitKey
        
        mock_detector.detectAndDecode.return_value = ("invalid-code", "bbox", None)
        mock_verify.return_value = False
        
        # Side effect for waitKey: return 'q' (ord('q')) to break loop
        mock_wait.return_value = ord('q')

        # Execute
        # We patch time.sleep to run fast
        with patch('scanner.time.sleep') as mock_sleep:
            scanner.scan_qr_code()
            
            # Assertions
            mock_verify.assert_called_with("invalid-code")
            # If verify fails, sleep is called
            mock_sleep.assert_called()
            mock_cap.release.assert_called_once()

    @patch('scanner.cv2.VideoCapture')
    def test_camera_not_opened(self, mock_video_capture):
        mock_cap = MagicMock()
        mock_video_capture.return_value = mock_cap
        mock_cap.isOpened.return_value = False
        
        # Execute
        scanner.scan_qr_code()
        
        # Assertions
        mock_cap.isOpened.assert_called_once()
        mock_cap.read.assert_not_called()

if __name__ == '__main__':
    unittest.main()
