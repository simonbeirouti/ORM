# ORM lesson

Object-Relational Mapping is a technique that lets you query and manipulate data from a database using object-orientated paradigms. In projects, having an ORM in places means you can easily switch out the database for another type and continue to operate the application without any issues (ideally).

## CRUD

Create, Read, Update and Destroy is what all databases will mainly focus on when needed to work alongside side an application.

## Steps

### Setup application

1. `virtualenv venv` or `source venv/bin/activate`
2. `touch app.py`
3. `pip3 install flask`
4. `pip freeze > requirements.txt`

### Setup database

1. `psql -U postgres` # Connect to postgres
2. `create database 'name_of_db';` # Create database
3. `\c name_of_db` # Change into database
4. `create user 'main_use'r with password '123qwe';` # Create user
5. `grant all privileges on database 'name_of_db' to 'main_use'r;` # Assign user all privileges on database
6. `pip3 install psycopg2 flask-sqlalchemy` # Packages to ORM flask to postgresql
