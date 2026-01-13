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

**How to start the database**

1.Install PostgreSQL and pgAdmin

https://www.postgresql.org/download/windows/

2.Create .env file
```
DB_NAME=your_database_name
DB_USER=your_username
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432
```

3.Create database in PostgreSQL

In pgAdmin:
```
Servers -> PostgreSQL -> Databases -> Right-click -> Create -> Database
```
The Name must exactly match the DB_NAME value in your .env file.

4.Install Dependencies and Run Setup Script
```
pip install -r requirements.txt
python db_setup.py
```

**How to run the application**

#### Backend
```
uvicorn api.main:app --reload
```

#### Frontend
```
npm run dev
```