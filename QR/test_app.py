import generator
import database
import os

def test_generator_and_db():
    print("Testing Generator and Database...")
    
    # Clean up potential previous test run
    if os.path.exists("qr_codes.db"):
        # We won't delete it to avoid losing user data if they ran it, 
        # but for a clean test we might want to use a test db.
        # For now, we just rely on unique IDs.
        pass

    # Generate a code
    filename = generator.generate_qr_code()
    
    if filename and os.path.exists(filename):
        print(f"PASS: File {filename} created.")
        
        # Extract ID from filename (format: qr_<uuid>.png)
        code_id = filename.replace("qr_", "").replace(".png", "")
        
        # Verify in DB
        if database.verify_code(code_id):
            print(f"PASS: Code {code_id} found in database.")
        else:
            print(f"FAIL: Code {code_id} NOT found in database.")
            
        # Clean up image
        os.remove(filename)
        print("Test cleanup: Removed generated image.")
    else:
        print("FAIL: Image file not created.")

if __name__ == "__main__":
    test_generator_and_db()
