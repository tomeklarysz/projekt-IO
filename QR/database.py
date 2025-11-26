import sqlite3
import os

DB_NAME = "qr_codes.db"

def init_db():
    """Initialize the database and create the table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS codes (
            id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_code(code_id):
    """Save a new code identifier to the database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO codes (id) VALUES (?)', (code_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print(f"Database error: {e}")
        return False

def verify_code(code_id):
    """Verify if a code identifier exists in the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM codes WHERE id = ?', (code_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def delete_code(code_id):
    """Delete a code identifier from the database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM codes WHERE id = ?', (code_id,))
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        return deleted_count > 0
    except Exception as e:
        print(f"Database error: {e}")
        return False
