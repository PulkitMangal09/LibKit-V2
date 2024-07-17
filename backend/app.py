from flask import Flask
from Applications.database import db
from Applications.api import api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from Applications.api import init_app

app = None

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///LibKit.sqlite3'
    app.config['JWT_SECRET_KEY']='super-secret' # Change this in your code
    jwt=JWTManager(app)
    CORS(app)
    
    # Set the upload folder configuration
    app.config['UPLOAD_FOLDER'] = 'C:\\Users\\pulki\\OneDrive\\Documents\\MAD 1 Proj\\static\\images'
    db.init_app(app) # Equivalent to write db = SQLAlchemy(app) in database.py
    init_app(app) # Equivalent to write api = Api(app) in api.py
    app.app_context().push()

    return app

app = create_app()

from Applications.controller import *  # Models are imported in controller.py and controllers are imported here
from Applications.user_controller import *
from Applications.admin_controller import *

if __name__ == '__main__':

    with app.app_context():
        db.create_all()
        try:
            user = User(name='admin', username='admin', email='admin@admin', password=generate_password_hash('1234'), type='admin')
            db.session.add(user)
            db.session.commit()
        except:
            pass

    app.run()
