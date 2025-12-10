import psycopg2
from database.db_setup import get_db_connection

def get_employee_face_data(employee_id):
    """
    Fetches the vector_features and photo_path for a given employee_id.
    Returns a tuple (vector_features, photo_path) or None if not found.
    """
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT first_name, vector_features, photo_path FROM employees WHERE id = %s",
            (employee_id,)
        )
        result = cur.fetchone()
        return result # (vector_features, photo_path)
    except Exception as e:
        print(f"Error fetching employee face data: {e}")
        return None
    finally:
        conn.close()

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
            "SELECT id, first_name, vector_features, photo_path FROM employees WHERE qr_hash = %s",
            (qr_hash,)
        )
        result = cur.fetchone()
        if result:
            return {
                "id": result[0],
                "first_name": result[1],
                "vector_features": result[2],
                "photo_path": result[3]
            }
        return None
    except Exception as e:
        print(f"Error fetching employee by QR: {e}")
        return None
    finally:
        conn.close()

def update_employee_vector(employee_id, vector_features):
    """
    Updates the vector_features for a given employee_id.
    Useful if we want to cache the computed vector from the photo.
    """
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        # Convert numpy array to list if necessary, though psycopg2 handles lists
        if hasattr(vector_features, 'tolist'):
            vector_features = vector_features.tolist()
            
        cur.execute(
            "UPDATE employees SET vector_features = %s WHERE id = %s",
            (vector_features, employee_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating employee vector: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def upsert_employee_vector(employee_id, vector_features, first_name=None, last_name=None, qr_hash=None, photo_path=None):
    """
    Updates the vector_features for a given employee_id.
    If the employee does not exist and required fields are provided, inserts a new employee.
    
    Returns:
        "Updated" if updated.
        "Created" if inserted.
        "Not Found" if not found and cannot insert.
        "Error" if an exception occurred.
    """
    conn = get_db_connection()
    if not conn:
        return "Error"
    
    try:
        cur = conn.cursor()
        # Convert numpy array to list if necessary
        if hasattr(vector_features, 'tolist'):
            vector_features = vector_features.tolist()
            
        # Try Update
        cur.execute(
            "UPDATE employees SET vector_features = %s, photo_path = %s WHERE id = %s",
            (vector_features, photo_path, employee_id)
        )
        
        if cur.rowcount > 0:
            conn.commit()
            return "Updated"
            
        # If not updated, check if we can insert
        if first_name and last_name and qr_hash:
            # We have enough info to insert
            # Note: photo_path is optional in schema but good to have if we used it to generate vector
            cur.execute(
                """
                INSERT INTO employees (id, first_name, last_name, qr_hash, vector_features, photo_path)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (employee_id, first_name, last_name, qr_hash, vector_features, photo_path)
            )
            conn.commit()
            return "Created"
        else:
            return "Not Found"
            
    except Exception as e:
        print(f"Error upserting employee vector: {e}")
        conn.rollback()
        return "Error"
    finally:
        conn.close()
