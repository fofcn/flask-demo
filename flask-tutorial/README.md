# create a python venv
```shell
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

# Initialize the database file
```shell
flask --app flaskr init-db
```

# run the application
```shell
flask --app flaskr run --debug
```