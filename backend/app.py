from flask import Flask, send_from_directory
from Applications.database import db
from Applications.api import api, init_app
from Applications.config import jwt, cache, cors
from werkzeug.security import generate_password_hash
from Applications.worker import celery_init_app
from Applications.tasks import check_visited_users, generate_monthly_report
from celery.schedules import crontab

app = None

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///LibKit.sqlite3'
    app.config['JWT_SECRET_KEY']='super-secret' # Change this in your code
    jwt.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})

    
    # Set the upload folder configuration
    app.config['UPLOAD_FOLDER'] = 'C:\\Users\\pulki\\OneDrive\\Documents\\export_check'

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
    
    # Initialize the worker
    celery_app=celery_init_app(app)

    return app, celery_app

app, celery_app = create_app()

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    
    # Executes every day at 6:00 PM (18:00)
    sender.add_periodic_task(crontab(hour=18, minute=0),
                             check_visited_users.s(), 
                             name='Check visited users every day at 6 PM'
                             )
    
    # Executes on the first day of every month at midnight (00:00)
    sender.add_periodic_task(crontab(day_of_month=1, hour=0, minute=0), 
                             generate_monthly_report.s(), 
                             name='Generate monthly report on the first day of every month at midnight'
                             )


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
