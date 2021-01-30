https://flask.palletsprojects.com/en/1.1.x/installation/

Create a virtual environment following the instructions in the link above, making sure to have all the dependencies specified in "requirements.txt".

Create an environment
Create a project folder and a venv folder within:
```
py -3 -m venv venv
venv\Scripts\activate
```

Install Dependencies
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

2. Run flask:
```
cd server/flask_server
set FLASK_APP=main.py 
set APP_SETTINGS=config.DevelopmentConfig
flask run
```

For changes in the database model:
```
python manage.py db migrate
python manage.py db upgrade
#Only when there are problems upgrading the db and repeat the two first steps
python manage.py db stamp head
```
