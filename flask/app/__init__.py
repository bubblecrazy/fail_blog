from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_pagedown import PageDown
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    #sqlite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'a9087FFJFF9nnvc2@#$%FSD'
app = Flask(__name__)

login = LoginManager(app)
login.login_view = 'login'
app.config.from_object(Config)

#建立数据库关系
db = SQLAlchemy(app)
#绑定app和数据库，以便进行操作
migrate = Migrate(app,db)

pagedown = PageDown()
pagedown.init_app(app)
from app import routes,models

db.create_all()