## Setup

Make a python virtual environment
```
python3 -m venv venv
```
Activate the virtual environment
```
source venv/bin/activate
```
Install packages from requirements.txt
```
pip install -r requirements.txt
```
Create the file .env in the root and fill this in
```
340DBHOST=<your-database-host>
340DBUSER=<your-database-username>
340DBPW=<your-database-password>
340DB=<your-database-name>
```
Run app.py :)
You will be able to access it at the port specified at the end of app.py
