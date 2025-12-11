from db_operations import get_status_by_qr_hash, toggle_status_by_qr_hash, delete_employee_by_qr_hash, add_employee

emp_id = add_employee("karol", "xxxx", "..\images\img1.jpg")

# test_qr = "498eb7fa-c3a4-40fe-8c75-1e9108d1e717"
# print("\n--- Sprawdzenie Statusu ---")
# initial_status = get_status_by_qr_hash(test_qr)
# print(f"Initial status: {initial_status}") 

# print("\n--- Zmiana Statusu (Toggle) ---")
# toggle_status_by_qr_hash(test_qr)

# new_status = get_status_by_qr_hash(test_qr)
# print(f"Status po zmianie: {new_status}")

#print("\n--- Usuwanie ---")
#delete_employee_by_qr_hash(test_qr)

#print("\n--- Weryfikacja Usunięcia ---")
#deleted_check = get_status_by_qr_hash(test_qr)
#print(f"Status po usunięciu: {deleted_check}")
