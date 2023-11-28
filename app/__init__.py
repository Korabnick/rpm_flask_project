from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import getenv
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 604800
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = getenv('USER_MAIL')
app.config['MAIL_PASSWORD'] = getenv('PASS_MAIL')
app.config['MAIL_DEFAULT_SENDER'] = getenv('USER_MAIL')
app.config['MAIL_USE_TLS'] = True

mail = Mail(app)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)


from app import routes
