https://flask.palletsprojects.com/en/1.1.x/installation/

Create a virtual environment following the instructions in the link above, making sure to have all the dependencies specified in "requirements.txt". You can also follow the instructions below.

Create an environment<br/>
Inside the folder "server":
```
py -3 -m venv venv
venv\Scripts\activate
```

Install Dependencies<br/>
Within the activated environment, use the following command to install all dependencies
```
pip install -r requirements.txt
```

To run server
1. Activate virtual environment:
```
activate virtual environment (venv)
cd venv/Scripts
activate.bat
```

2.a Run flask on CMD console:
```
cd flask_server
set FLASK_APP=main.py 
set FLASK_ENV=development
set APP_SETTINGS=flask_server.config.Config
flask run
```
2.b Run flask on powershell console:
```
cd flask_server
$env:FLASK_APP = "main.py"
$env:FLASK_ENV = "development"
$env:APP_SETTINGS="flask_server.config.Config"
flask run
```
2.c Run flask on Linux console:
```
cd flask_server
export FLASK_APP=main.py
export FLASK_ENV=development
export APP_SETTINGS=flask_server.config.Config
flask run
```
3 For changes in the database model:
```
flask db migrate
flask db upgrade
#Only when there are problems upgrading the db and repeat the two first steps
flask db stamp head
```

To run the whole project locally, it is necessary to have a local postgres database and possibly changing config.py line 10:
```
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://angelly:123@127.0.0.1:5432/clup_DB"
```
Creating a database with the name clup_DB with the same user "angelly" and password "123" or different user and changing config.py

To test it is necessary to create a test database name 'clup_test_DB'
*Consider that the commands for changes in the database are different
Also run again step (2)
