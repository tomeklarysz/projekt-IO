Create virtual environment and install requirements:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Setup database:
```
python db_setup.py
```

Add employee to database (make sure to fill all fields for employee and provide path to photo):
```
python manage_employees.py
```

Run authentication system against your camera:
```
python main.py
```