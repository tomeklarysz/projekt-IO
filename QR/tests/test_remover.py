import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Adjust path to import remover module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import remover

class TestRemover(unittest.TestCase):
    
    @patch('remover.cv2.VideoCapture')
    @patch('remover.cv2.QRCodeDetector')
    @patch('remover.database.init_db')
    @patch('remover.database.verify_code')
    @patch('remover.database.delete_code')
    @patch('remover.cv2.imshow')
    @patch('remover.cv2.waitKey')
    @patch('remover.cv2.destroyAllWindows')
    def test_remove_qr_code_success(self, mock_destroy, mock_wait, mock_imshow, mock_delete, mock_verify, mock_init, mock_detector_cls, mock_video_capture):
        # Setup mocks
        mock_cap = MagicMock()
        mock_video_capture.return_value = mock_cap
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, "fake_frame")
        
        mock_detector = MagicMock()
        mock_detector_cls.return_value = mock_detector
        
        # Detect a code
        mock_detector.detectAndDecode.return_value = ("code-to-remove", "bbox", "rectified")
        
        # Verify finds it, Delete succeeds
        mock_verify.return_value = True
        mock_delete.return_value = True
        
        # Execute
        remover.remove_qr_code()
        
        # Assertions
        mock_verify.assert_called_with("code-to-remove")
        mock_delete.assert_called_with("code-to-remove")
        # Should break loop after success
        mock_cap.release.assert_called_once()
        mock_destroy.assert_called_once()

    @patch('remover.cv2.VideoCapture')
    @patch('remover.cv2.QRCodeDetector')
    @patch('remover.database.init_db')
    @patch('remover.database.verify_code')
    @patch('remover.database.delete_code')
    @patch('remover.cv2.imshow')
    @patch('remover.cv2.waitKey')
    @patch('remover.cv2.destroyAllWindows')
    def test_remove_qr_code_found_but_delete_fails(self, mock_destroy, mock_wait, mock_imshow, mock_delete, mock_verify, mock_init, mock_detector_cls, mock_video_capture):
        # Setup mocks
        mock_cap = MagicMock()
        mock_video_capture.return_value = mock_cap
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, "fake_frame")
        
        mock_detector = MagicMock()
        mock_detector_cls.return_value = mock_detector
        
        # Detect a code
        mock_detector.detectAndDecode.return_value = ("code-fail-delete", "bbox", "rectified")
        
        # Verify true, but delete false
        mock_verify.return_value = True
        mock_delete.return_value = False
        
        # Execute
        remover.remove_qr_code()
        
        # Assertions
        mock_delete.assert_called_with("code-fail-delete")
        # Should still break loop? 
        # Looking at code:
        # if database.delete_code(data): ... break
        # else: ... break
        # So yes, it breaks in both cases.
        mock_cap.release.assert_called_once()

if __name__ == '__main__':
    unittest.main()
