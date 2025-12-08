import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Adjust path to import generator module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import generator

class TestGenerator(unittest.TestCase):
    
    @patch('generator.database.init_db')
    @patch('generator.database.save_code')
    @patch('generator.qrcode.QRCode')
    @patch('generator.uuid.uuid4')
    def test_generate_qr_code_success(self, mock_uuid, mock_qrcode_cls, mock_save_code, mock_init_db):
        # Setup mocks
        mock_uuid.return_value = "test-uuid"
        mock_save_code.return_value = True
        
        mock_qr_instance = MagicMock()
        mock_qrcode_cls.return_value = mock_qr_instance
        
        mock_img = MagicMock()
        mock_qr_instance.make_image.return_value = mock_img
        
        # Execute
        filename = generator.generate_qr_code()
        
        # Assertions
        mock_init_db.assert_called_once()
        mock_save_code.assert_called_once_with("test-uuid")
        
        # Check qrcode calls
        mock_qrcode_cls.assert_called_once()
        mock_qr_instance.add_data.assert_called_once_with("test-uuid")
        mock_qr_instance.make.assert_called_once_with(fit=True)
        mock_qr_instance.make_image.assert_called_once()
        
        # Check file saving
        expected_filename = "qr_test-uuid.png"
        mock_img.save.assert_called_once_with(expected_filename)
        self.assertEqual(filename, expected_filename)

    @patch('generator.database.init_db')
    @patch('generator.database.save_code')
    @patch('generator.uuid.uuid4')
    def test_generate_qr_code_db_fail(self, mock_uuid, mock_save_code, mock_init_db):
        # Setup mocks
        mock_uuid.return_value = "test-uuid"
        mock_save_code.return_value = False # Simulate DB failure
        
        # Execute
        filename = generator.generate_qr_code()
        
        # Assertions
        mock_init_db.assert_called_once()
        mock_save_code.assert_called_once_with("test-uuid")
        self.assertIsNone(filename)

if __name__ == '__main__':
    unittest.main()
