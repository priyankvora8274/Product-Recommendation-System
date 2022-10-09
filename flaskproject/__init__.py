
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'ee9aa3afd91c6965cfb2649caf297f2f'

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view= 'login'

from flaskproject import routes 