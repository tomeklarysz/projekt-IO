import argparse
import sys
from face_auth.admin import upsert_employee_from_photo

def main():
    
    # for testing purposes update this
    args = {
        "photo_path": "",
        "employee_id": 1,
        "first_name": "",
        "last_name": "",
        "qr_hash": ""
    }
    
    print(f"Processing employee ID {args['employee_id']} with photo {args['photo_path']}...")
    
    result = upsert_employee_from_photo(
        args['photo_path'],
        args['employee_id'],
        first_name=args['first_name'],
        last_name=args['last_name'],
        qr_hash=args['qr_hash']
    )
    
    if result == "Updated":
        print("Successfully updated existing employee face vector.")
    elif result == "Created":
        print("Successfully created new employee with face vector.")
    elif result == "Not Found":
        print("Error: Employee not found and missing required fields (first_name, last_name, qr_hash) to create new.")
        sys.exit(1)
    elif result.startswith("Error"):
        print(result)
        sys.exit(1)
    else:
        print(f"Unexpected result: {result}")
        sys.exit(1)

if __name__ == "__main__":
    main()
