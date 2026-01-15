from database.db_operations import  delete_employee_by_qr_hash, add_employee, get_employee_id_by_qr, log_verification_event, get_latest_status, get_logs

#emp_id1 = add_employee("a", "a", ".\images\img1.jpg")
#emp_id1 = add_employee("z", "z", ".\images\img2.png")

qr_hash1 = "19ee93d6-eb20-4988-8e31-fd6ddc829c7c"
qr_hash2 = "9ca853fe-7150-4b3c-b669-a8634410454c"

id1 = get_employee_id_by_qr(qr_hash1)
id2 = get_employee_id_by_qr(qr_hash2)

# get_logs(id1)
# get_logs(id2)

delete_employee_by_qr_hash(qr_hash2)

#get_logs(id2)