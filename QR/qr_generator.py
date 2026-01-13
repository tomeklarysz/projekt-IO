import uuid
import qrcode
import os
from datetime import datetime, timedelta
from typing import Tuple

QR_CODE_DIR = "generated_qrs"
os.makedirs(QR_CODE_DIR, exist_ok=True)


def generate_unique_qr_hash():
    return str(uuid.uuid4())

def create_qr_expiration_date():
    return (datetime.now() + timedelta(days=180)).date()

def create_qr_image(qr_hash, filename_prefix):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_hash) 
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        filename = f"{QR_CODE_DIR}/{filename_prefix}.png"
        img.save(filename)
        
        return filename

    except Exception as e:
        print(f"QR code generation error for hash {qr_hash}: {e}")
        return None