from db_operations import get_status_by_qr_hash, toggle_status_by_qr_hash, delete_employee_by_qr_hash, add_employee

emp_id = add_employee("first_name_test", "last_name_test", [1, 2, 3], "photo_path")

#print("\n--- Sprawdzenie Statusu ---")
#initial_status = get_status_by_qr_hash(test_qr)
#print(f"Initial status: {initial_status}") 

#rint("\n--- Zmiana Statusu (Toggle) ---")
#oggle_status_by_qr_hash(test_qr)

#ew_status = get_status_by_qr_hash(test_qr)
#rint(f"Status po zmianie: {new_status}")

#print("\n--- Usuwanie ---")
#delete_employee_by_qr_hash(test_qr)

#print("\n--- Weryfikacja Usunięcia ---")
#deleted_check = get_status_by_qr_hash(test_qr)
#print(f"Status po usunięciu: {deleted_check}")
