from fastapi import FastAPI, HTTPException, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import shutil
import os

# Imports from your modules (ensure paths are correct)
from database.db_operations import (
    add_employee, 
    get_employee_by_qr, 
    delete_employee_by_qr_hash,
    update_expiry_by_qr_hash,
    get_all_employees,
    update_employee_info
)
from database.queries import upsert_employee_vector
from api.schemas import EmployeeResponse, StatusResponse, VectorUpdate, ExpiryRequest

app = FastAPI(title="Face Auth System API")

# CORS configuration - allows communication with web applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directories exist
os.makedirs("generated_qrs", exist_ok=True)
os.makedirs("images", exist_ok=True)

# Mount static files to serve images and QRs
app.mount("/generated_qrs", StaticFiles(directory="generated_qrs"), name="generated_qrs")
app.mount("/images", StaticFiles(directory="images"), name="images")

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"message": "API is running correctly without creating local folders"}

@app.get("/api/workers")
def get_workers_endpoint():
    """
    Returns a list of all workers (employees) with their name and status.
    """
    workers = get_all_employees()
    return workers

@app.post("/upload")
async def upload_photo(file: UploadFile = File(...)):
    try:
        os.makedirs("images", exist_ok=True)
        # Use simple filename or add timestamp to prevent collisions in production
        file_location = f"images/{file.filename}"
        
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Return relative path, e.g. "images/filename.jpg"
        # This allows the database to store a clean relative path instead of an absolute system path.
        return {"file_path": file_location}
    except Exception as e:
        print(f"Upload Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/employees/add")
def create_employee_endpoint(
    first_name: str = Form(...),
    last_name: str = Form(...),
    photo_path: str = Form(...)
):
    """
    Adds an employee based on an existing file path on the disk.
    Accepts Form data: first_name, last_name, photo_path
    """
    try:
        # Calls add_employee, which uses recognizer.load_image_file(photo_path) internally
        new_id = add_employee(first_name, last_name, photo_path)
        
        if new_id is None:
            # If database insertion or face detection failed, delete the uploaded image
            if os.path.exists(photo_path):
                try:
                    os.remove(photo_path)
                    print(f"Cleanup: Deleted file {photo_path} due to registration failure.")
                except OSError as cleanup_error:
                    print(f"Cleanup Error: Failed to delete {photo_path}: {cleanup_error}")

            raise HTTPException(
                status_code=500, 
                detail="Error: Face not detected in the image or database error. Image file has been removed."
            )
            
        return {
            "id": new_id, 
            "message": f"Employee added successfully. Used image from: {photo_path}"
        }
        
    except Exception as e:
        # If any unexpected exception occurs, also attempt to clean up the image
        if os.path.exists(photo_path):
            try:
                os.remove(photo_path)
                print(f"Cleanup: Deleted file {photo_path} due to exception.")
            except OSError as cleanup_error:
                print(f"Cleanup Error: Failed to delete {photo_path}: {cleanup_error}")
                
        # Log error to server console for easier debugging
        print(f"API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/employees/expiry")
def update_expiry_endpoint(request: ExpiryRequest):
    success = update_expiry_by_qr_hash(request.qr_hash, request.new_expiry_date)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found to update expiry")
    return {"message": "Expiry date updated successfully"}

@app.get("/employees/{qr_hash}", response_model=EmployeeResponse)
def get_employee_endpoint(qr_hash: str):
    employee_data = get_employee_by_qr(qr_hash)
    if not employee_data:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee_data

@app.put("/employees/{qr_hash}")
def update_employee_endpoint(
    qr_hash: str,
    first_name: str = Form(None),
    last_name: str = Form(None),
    photo_path: str = Form(None)
):
    success = update_employee_info(qr_hash, first_name, last_name, photo_path)
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update employee. Check if employee exists or if photo is valid.")
        
    return {"message": "Employee updated successfully"}




@app.get("/employees/status/{qr_hash}")
def get_status_endpoint(qr_hash: str):
    status = get_status_by_qr_hash(qr_hash)
    if status is None:
        raise HTTPException(status_code=404, detail="Invalid QR code")
    return {"is_confirmed": status}

@app.post("/employees/toggle/{qr_hash}", response_model=StatusResponse)
def toggle_status_endpoint(qr_hash: str):
    new_status = toggle_status_by_qr_hash(qr_hash)
    if new_status is None:
        raise HTTPException(status_code=404, detail="Employee not found to change status")
    return {"qr_hash": qr_hash, "is_confirmed": new_status}

@app.delete("/employees/{qr_hash}")
def delete_employee_endpoint(qr_hash: str):
    success = delete_employee_by_qr_hash(qr_hash)
    if not success:
        raise HTTPException(status_code=404, detail="Employee could not be deleted (might not exist)")
    return {"message": "Employee deleted successfully"}

@app.post("/vectors/upsert")
def upsert_vector_endpoint(data: VectorUpdate):
    """
    Allows manual update of feature vectors.
    """
    import numpy as np
    vector_np = np.array(data.vector_features)
    
    result = upsert_employee_vector(
        employee_id=data.employee_id,
        vector_features=vector_np,
        first_name=data.first_name,
        last_name=data.last_name,
        qr_hash=data.qr_hash,
        photo_path=data.photo_path
    )
    return {"status": result}

@app.get("/api/employees/logs/{qr_hash}")
def get_employee_logs_endpoint(qr_hash: str):
    """
    Fetches the log history for an employee based on their QR hash.
    """
    from database.db_operations import get_employee_id_by_qr, get_logs
    
    employee_id = get_employee_id_by_qr(qr_hash)
    
    if employee_id is None:
        raise HTTPException(status_code=404, detail="Employee with the provided QR code does not exist.")

    logs = get_logs(employee_id)
    
    if logs is None:
        return [] 
    
    formatted_logs = []
    for row in logs:
        formatted_logs.append({
            "first_name": row[0],
            "last_name": row[1],
            "status": row[2],
            "event_time": row[3], 
            "reason": row[4]
        })
    
    return formatted_logs

@app.get("/api/logs/all")
def get_all_logs_endpoint():
    """Fetches all verification logs from the database for all employees."""
    from database.db_operations import get_db_connection
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT e.first_name, e.last_name, v.status, v.event_time, v.reason 
            FROM verification_logs v
            JOIN employees e ON v.employee_id = e.id
            ORDER BY v.event_time DESC;
        """)
        rows = cur.fetchall()
        return [{"first_name": r[0], "last_name": r[1], "status": r[2], 
                 "event_time": r[3], "reason": r[4]} for r in rows]
    finally:
        cur.close()
        conn.close()