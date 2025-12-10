import psycopg2
from db_setup import get_db_connection
from pathlib import Path
import sys
import os

current_dir = Path(__file__).resolve().parent 
project_root = current_dir.parent 
sys.path.append(str(project_root))

import QR.qr_generator as qr_generator

def add_employee(first_name, last_name, vector_features, photo_path):
    qr_hash = qr_generator.generate_unique_qr_hash()
    print(f"Generated QR Hash: {qr_hash}")
    
    conn = get_db_connection()
    if not conn:
        return None

    cur = conn.cursor()
    employee_id = None
    try:
        cur.execute("""
            INSERT INTO employees (first_name, last_name, qr_hash, vector_features, photo_path)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """, (first_name, last_name, qr_hash, vector_features, photo_path))

        employee_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO verification_statuses (employee_id, is_confirmed)
            VALUES (%s, FALSE);
        """, (employee_id,))

        conn.commit()
        print(f"Employee inserted with ID: {employee_id}")

        filename_prefix = f"qr_{first_name}_{last_name}"
        qr_file_path = qr_generator.create_qr_image(qr_hash, filename_prefix)
        
        if qr_file_path:
            print(f"QR Code generated and saved to: {qr_file_path}")
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