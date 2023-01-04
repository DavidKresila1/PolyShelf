from pydoc_data.topics import topics
from flask import Flask
from flask_login import LoginManager
import socket
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_basicauth import BasicAuth
from admin import DefaultModelView, MyAdminIndexView
from flask_admin.menu import MenuLink
from flask_sqlalchemy import SQLAlchemy
from models import db, User



def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP 

app = Flask(__name__)





app.config["SECRET_KEY"] = "dgasdkg654fegkhf"
appRoot = os.path.dirname(os.path.abspath(__file__))
uploadFolder = os.path.join(appRoot, "data")

app.config["UPLOAD_FOLDER"] = uploadFolder

app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    SESSION_COOKIE_PATH='/',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
))

app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config.from_object(__name__)
app.config.from_envvar("FLASKR_SETTINGS", silent=True)


loginManager = LoginManager()
loginManager.login_view = "auth.login"
loginManager.init_app(app)

db.create_all()



def create_app():
    

    from models import User


    @loginManager.user_loader
    def load_user(user_id):
        return db.query(User).get(int(user_id))


    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #from admin import admin as admin_blueprint
    #app.register_blueprint(admin_blueprint)

    
    admin = Admin(app, name='Dashboard')
    admin.add_view(ModelView(User, db.session))


    app.run(getIP(), port=8000, debug=True)

    @app.errorhandler(404)
    def page_not_found(_):
        return "404"





if __name__ == "__main__":
    create_app()