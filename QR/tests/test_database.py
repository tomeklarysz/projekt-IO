import unittest
import os
import sys
import sqlite3

import tempfile
import time
import shutil

# Adjust path to import database module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Use a temporary database for testing in a temp directory
        self.test_dir = tempfile.mkdtemp()
        self.test_db = os.path.join(self.test_dir, "test_qr_codes.db")
        self.original_db_name = database.DB_NAME
        database.DB_NAME = self.test_db
        database.init_db()

    def tearDown(self):
        # Restore original DB name and remove test dir
        database.DB_NAME = self.original_db_name
        
        # Ensure connections are closed (handled by app code, but file might be locked by OS/AV)
        time.sleep(0.1) 
        
        try:
            shutil.rmtree(self.test_dir)
        except PermissionError:
            print(f"Warning: Could not remove test dir {self.test_dir}")

    def test_init_db(self):
        # Verify table creation
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='codes';")
        table_exists = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(table_exists)

    def test_save_code(self):
        code_id = "test-uuid-1234"
        result = database.save_code(code_id)
        self.assertTrue(result)
        
        # Verify it's actually in DB
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM codes WHERE id=?", (code_id,))
        row = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], code_id)

    def test_save_duplicate_code(self):
        # Saving same code twice should fail (or return False depending on implementation)
        code_id = "unique-id"
        database.save_code(code_id)
        result = database.save_code(code_id)
        self.assertFalse(result)

    def test_verify_code(self):
        code_id = "valid-id"
        database.save_code(code_id)
        
        self.assertTrue(database.verify_code(code_id))
        self.assertFalse(database.verify_code("invalid-id"))

    def test_delete_code(self):
        code_id = "to-be-deleted"
        database.save_code(code_id)
        
        self.assertTrue(database.verify_code(code_id))
        
        result = database.delete_code(code_id)
        self.assertTrue(result)
        self.assertFalse(database.verify_code(code_id))

    def test_delete_nonexistent_code(self):
        result = database.delete_code("non-existent")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
