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
            "SELECT vector_features, photo_path FROM employees WHERE id = %s",
            (employee_id,)
        )
        result = cur.fetchone()
        return result # (vector_features, photo_path)
    except Exception as e:
        print(f"Error fetching employee face data: {e}")
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
