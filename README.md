# Authentication using JWT Tokens between React and Django using Simple JWT

  * The purpose of this project is to implement user authentication using JWT (JSON Web Tokens) between a React frontend and a Django backend. The authentication process will be handled using the Simple JWT library in Django.We are going to take advantage of Django Rest Framework and other in built modules

# Core Technologies and Libraries Used

Technology/Library | Description 
--- | --- |
*Django REST Framework* | *Api building framework for django*
*SQLite3* | *A database service*
*Django* | *A python framework for building serverside applications*
*React* | *A Javascript library for building client side applications*

  

# Setting up the codebase locally

This is a step by step guide on how to set up the codebase locally

Clone the project
----------------------
``` shellgit@github.com:daisy-carolin/ACTSVC.git
git clone https://github.com/Euniceatieno/HackCX.git
```
Set up your virtual environment
----------------------
``` shell
python3 -m venv env
```
Activate your virtual environment
----------------------
``` shell
source env/bin/activate
```
Install the required packages
----------------------
``` shell
python3 -m pip install -r requirements.txt --no-cache-dir
```
Create a .env file with the following environment variables
------------------------------------------------------------------
``` shell
SECRET_KEY=yoursecretkey
DATABASE_NAME=yourdb
DATABASE_USER=yourdbuser
DATABASE_PASSWORD=yourbdpassword
DATABASE_HOST=localhost
DATABASE_PORT=5432
```
Export your environment variables
--------------------------------------------
``` shell
source .env
source .env
```
Create a local database with the credentials in your .env file
---------------------------------------------------------------

Run migrations
----------------------
``` shell
python3 manage.py makemigrations
```
Migrate database updates
----------------------
``` shell
python3 manage.py migrate
```
Start local server
----------------------
``` shell
python3 manage.py runserver
```

# Contacts
For any queries ,reach out to either: 
 * *daissiodawa@gmail.com*




