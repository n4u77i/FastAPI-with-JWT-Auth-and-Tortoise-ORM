# FastAPI-with-JWT-Auth-and-Tortoise-ORM

This project was made to learn and implement the JWT auth in FastAPI with Tortoise-ORM.
Tortoise-ORM is just like Django-ORM or SQLAlchemy-ORM to interact with the database.
The _sqlite_ databse is used for this project.

To run the project, you need to first create virtualenv and activate it. Then install dependencies and run the project.
```
python3 -m venv venv-fast-api
source venv-fast-api/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

To use sqlite3 and generate table/schema
```
sqlite3 db.sqlite3
.schema
.exit
```

In case sqlite3 is not isntalled on your system then run `sudo apt-get install sqlite3 -y`
