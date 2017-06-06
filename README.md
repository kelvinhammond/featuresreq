# Installing requirements
This project requires python 3, it may work with python 2.7 though.
Install the requirements using pip.

`pip install -r requirements.txt`

# Running
Refer to the flask command line documentation or run it like this.

`FLASK_APP=featuresreq/app.py flask run`

*Note* the `FLASK_APP` requirement.

# Environment Variables
- `FLASK_APP`: should point to the app config file
- `FLASK_DEBUG`: will start the application in debug mode
- `FEATURES_REQ_DB_URI`: set the application database uri. See: [sqlalchemy engine configuration](http://docs.sqlalchemy.org/en/latest/core/engines.html)

# Testing
Run `py.test` from the root directory.

