from flask import Flask, send_from_directory
from Applications.database import db
from Applications.api import api, init_app
from Applications.config import jwt, cache, cors
from werkzeug.security import generate_password_hash

app = None

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///LibKit.sqlite3'
    app.config['JWT_SECRET_KEY']='super-secret' # Change this in your code
    jwt.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    
    # Set the upload folder configuration
    app.config['UPLOAD_FOLDER'] = 'C:\\Users\\pulki\\OneDrive\\Documents\\MAD 1 Proj\\static\\images'

    # Set the cache configuration

    # app.config['CACHE_TYPE'] = 'RedisCache'
    # app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    # app.config['CACHE_REDIS_PORT'] = 6379
    # app.config['DEBUG'] = True
    cache.init_app(app, config={'CACHE_TYPE': 'RedisCache', 'CACHE_DEFAULT_TIMEOUT': 300, 'CACHE_REDIS_PORT': 6379, 'DEBUG': True})

    # Initialize the cache

    db.init_app(app) # Equivalent to write db = SQLAlchemy(app) in database.py
    init_app(app) # Equivalent to write api = Api(app) in api.py
    app.app_context().push()

    @app.route('/static/images/<path:filename>')
    def serve_image(filename):
        return send_from_directory('static/images', filename)

    return app

app = create_app()

from Applications.controller import *  # Models are imported in controller.py and controllers are imported here


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
