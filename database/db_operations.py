import psycopg2
from .db_setup import get_db_connection
from pathlib import Path
import sys
import os

current_dir = Path(__file__).resolve().parent 
project_root = current_dir.parent 
sys.path.append(str(project_root))

import QR.qr_generator as qr_generator

from face_auth.recognizer import FaceRecognizer

def add_employee(first_name, last_name, photo_path): 
    """
    Generates a face vector from photo_path and inserts a new employee 
    record, verification status, and QR code into the database.
    
    Args:
        first_name (str): Employee's first name.
        last_name (str): Employee's last name.
        photo_path (str): File path to the employee's photo.
        
    Returns:
        int/None: The new employee ID on success, None on failure.
    """
    recognizer = FaceRecognizer()
    
    # --- 1. GENERATE FACE VECTOR FROM PHOTO ---
    
    print(f"Loading image from: {photo_path}")
    
    # Step 1: Load the image (using the recognizer's utility method)
    image = recognizer.load_image_file(photo_path)
    if image is None:
        print(f"Error: Could not load image from path: {photo_path}")
        return None
        
    # Step 2: Generate the face encoding (the vector)
    vector_features = recognizer.get_face_encoding(image)
    
    if vector_features is None:
        print("Error: Could not extract face features from the photo. Employee not added.")
        return None
        
    # Convert numpy array to list if required by the database driver
    if hasattr(vector_features, 'tolist'):
        vector_features = vector_features.tolist()
        
    # --- 2. DATABASE INSERTION ---
    
    qr_hash = qr_generator.generate_unique_qr_hash()
    qr_expiration_date = qr_generator.create_qr_expiration_date()
    print(f"Generated QR Hash: {qr_hash}")
    print(f"Generated QR Expiration Date: {qr_expiration_date}")
    
    conn = get_db_connection()
    if not conn:
        print("Error: Could not connect to the database.")
        return None

    cur = conn.cursor()
    employee_id = None
    try:
        # INSERT into employees table
        cur.execute("""
            INSERT INTO employees (first_name, last_name, qr_hash, vector_features, photo_path, qr_expiration_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (first_name, last_name, qr_hash, vector_features, photo_path, qr_expiration_date))

        employee_id = cur.fetchone()[0]

        # INSERT into verification_statuses table (default to unconfirmed)
        cur.execute("""
            INSERT INTO verification_statuses (employee_id, is_confirmed)
            VALUES (%s, FALSE);
        """, (employee_id,))

        conn.commit()
        print(f"Employee inserted with ID: {employee_id}")

        # --- 3. QR CODE GENERATION ---
        
        filename_prefix = f"qr_{first_name}_{last_name}"
        qr_file_path = qr_generator.create_qr_image(qr_hash, filename_prefix)
        
        if qr_file_path:
            print(f"QR Code generated and saved to: {qr_file_path}")
            # 
        else:
            print("WARNING: Failed to generate QR code image.")

        return employee_id

    except Exception as e:
        conn.rollback()
        print("Insert error:", e)
        return None
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_employee_id_by_qr(qr_hash):
    """Retrieves the employee ID based on their unique QR hash."""
    conn = get_db_connection()
    if not conn:
        return None

    cur = conn.cursor()
    employee_id = None
    try:
        cur.execute("""
            SELECT id
            FROM employees
            WHERE qr_hash = %s;
        """, (qr_hash,))

        result = cur.fetchone()
        employee_id = result[0] if result else None

    except Exception as e:
        print("ID query error:", e)
    finally:
        if conn:
            cur.close()
            conn.close()
        return employee_id
    
def get_employee_by_qr(qr_hash):
    """
    Fetches the employee data by QR hash.
    Returns a dictionary with keys: id, first_name, vector_features, photo_path, or None if not found.
    """
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, first_name, vector_features, photo_path, qr_expiration_date FROM employees WHERE qr_hash = %s",
            (qr_hash,)
        )
        result = cur.fetchone()
        if result:
            return {
                "id": result[0],
                "first_name": result[1],
                "vector_features": result[2],
                "photo_path": result[3],
                "qr_expiration_date": result[4],
                "qr_hash": qr_hash
            }
        return None
    except Exception as e:
        print(f"Error fetching employee by QR: {e}")
        return None
    finally:
        conn.close()

def get_status(employee_id):
    """Retrieves the latest verification status by employee ID."""
    conn = get_db_connection()
    if not conn:
        return

    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT is_confirmed
            FROM verification_statuses
            WHERE employee_id = %s
            ORDER BY id DESC LIMIT 1;
        """, (employee_id,))

        result = cur.fetchone()
        return result[0] if result else None

    except Exception as e:
        print("Query error:", e)
    finally:
        cur.close()
        conn.close()

def update_expiry_by_qr_hash(qr_hash, new_expiry_date):
    """Updates the QR expiration date for a specific employee."""
    conn = get_db_connection()
    if not conn:
        return False

    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE employees
            SET qr_expiration_date = %s
            WHERE qr_hash = %s;
        """, (new_expiry_date, qr_hash))

        conn.commit()
        return True
    except Exception as e:
        print("Update error:", e)
        conn.rollback()
        return False
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_status_by_qr_hash(qr_hash):
    """Retrieves the verification status based on the QR hash."""
    employee_id = get_employee_id_by_qr(qr_hash)
    if employee_id is None:
        print(f"Status Error: Employee with QR {qr_hash} does not exist.")
        return None
    
    return get_status(employee_id)


def toggle_status_by_qr_hash(qr_hash):
    """Toggles the verification status of an employee identified by QR hash."""
    employee_id = get_employee_id_by_qr(qr_hash)
    
    if employee_id is None:
        print(f"Error: Employee with QR hash {qr_hash} not found.")
        return None
    
    current_status = get_status(employee_id) 
    
    if current_status is None:
        print("Error: Could not retrieve current status.")
        return None
        
    new_status = not current_status

    conn = get_db_connection()
    if not conn:
        return None

    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE verification_statuses
            SET is_confirmed = %s
            WHERE employee_id = %s;
        """, (new_status, employee_id))

        conn.commit()
        print(f"Employee status (ID: {employee_id}, QR: {qr_hash}) changed to: {new_status}")
        return new_status

    except Exception as e:
        conn.rollback()
        print("Toggle error:", e)
    finally:
        if conn:
            cur.close()
            conn.close()

def delete_employee(employee_id):
    """Deletes an employee record by their ID (internal use)."""
    conn = get_db_connection()
    if not conn:
        return

    cur = conn.cursor()
    try:
        cur.execute("""
            DELETE FROM employees
            WHERE id = %s;
        """, (employee_id,))

        conn.commit()
        print(f"Employee {employee_id} removed.")

    except Exception as e:
        conn.rollback()
        print("Delete error:", e)
    finally:
        cur.close()
        conn.close()


def delete_employee_by_qr_hash(qr_hash):
    """Deletes an employee based on their QR hash."""
    employee_id = get_employee_id_by_qr(qr_hash)

    if employee_id is None:
        print(f"Deletion: Employee with QR hash {qr_hash} does not exist.")
        return False
    
    delete_employee(employee_id)
    return True