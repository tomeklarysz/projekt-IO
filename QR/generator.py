import uuid
import qrcode
import database
import os

def generate_qr_code():
    """
    Generates a new unique identifier, saves it to the database,
    and creates a QR code image.
    """
    # Ensure database is initialized
    database.init_db()

    # Generate unique ID
    code_id = str(uuid.uuid4())

    # Save to database
    if database.save_code(code_id):
        print(f"Generated ID: {code_id}")
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(code_id)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        filename = f"qr_{code_id}.png"
        img.save(filename)
        print(f"QR code saved as {filename}")
        return filename
    else:
        print("Failed to save code to database.")
        return None
