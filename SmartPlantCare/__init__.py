from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

from flask_login import LoginManager

import os
import psycopg2

app = Flask(__name__)


### Configuration για τα Secret Key, WTF CSRF Secret Key, SQLAlchemy Database URL, 
## Το όνομα του αρχείου της βάσης δεδομένων θα πρέπει να είναι 'flask_movies_database.db'
#app.config["SECRET_KEY"] = ''
app.config["SECRET_KEY"] = os.environ['SECRET_KEY']
#app.config['WTF_CSRF_SECRET_KEY'] = ''
app.config['WTF_CSRF_SECRET_KEY'] = os.environ['WTF_CSRF_SECRET_KEY']

#app.config["SQLALCHEMY_DATABASE_URI"] = ''
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['SQLALCHEMY_DATABASE_URI']

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


### Αρχικοποίηση της Βάσης, και άλλων εργαλείων ###

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

login_manager.login_view = "login_page"
login_manager.login_message_category = "warning"
login_manager.login_message = "Παρακαλούμε κάντε login για να μπορέσετε να δείτε αυτή τη σελίδα."


from SmartPlantCare import routes, models
