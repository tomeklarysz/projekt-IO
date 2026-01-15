from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware

# Imports from your modules (ensure paths are correct)
from database.db_operations import (
    add_employee, 
    get_employee_by_qr, 
    toggle_status_by_qr_hash, 
    delete_employee_by_qr_hash,
    get_status_by_qr_hash,
    update_expiry_by_qr_hash
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

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"message": "API is running correctly without creating local folders"}

@app.post("/employees/add")
def create_employee_endpoint(
    first_name: str = Form(...),
    last_name: str = Form(...),
    photo_path: str = Form(...)  # Path is received as text string, not binary file
):
    """
    Adds an employee based on an existing file path on the disk.
    """
    try:
        # Calls add_employee, which uses recognizer.load_image_file(photo_path) internally
        new_id = add_employee(first_name, last_name, photo_path)
        
        if new_id is None:
            raise HTTPException(
                status_code=500, 
                detail="Error: Face not detected in the image or database error."
            )
            
        return {
            "id": new_id, 
            "message": f"Employee added successfully. Used image from: {photo_path}"
        }
        
    except Exception as e:
        # Log error to server console for easier debugging
        print(f"API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/employees/{qr_hash}", response_model=EmployeeResponse)
def get_employee_endpoint(qr_hash: str):
    employee_data = get_employee_by_qr(qr_hash)
    if not employee_data:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee_data

@app.put("/employees/expiry")
def update_expiry_endpoint(request: ExpiryRequest):
    success = update_expiry_by_qr_hash(request.qr_hash, request.new_expiry_date)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found to update expiry")
    return {"message": "Expiry date updated successfully"}


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