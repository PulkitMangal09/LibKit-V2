# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask import current_app as app
# from .models import *
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
# import matplotlib.pyplot as plt
# from io import BytesIO
# from sqlalchemy import or_
# from werkzeug.utils import secure_filename
# import os
# import base64
# import datetime
# import numpy as np


# #Define the Login Manager
# login_manager = LoginManager(app)   

# app.config['SECRET_KEY'] = 'myverysecretkey'    


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))



# # Custom error handler for 401 Unauthorized
# @app.errorhandler(401)
# def unauthorized_error(error):
#     return render_template('UA.html', error='You are not authorized to view this page') , 401



# # Define the allowed extensions for image files
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# # Function to check if the filename has allowed extension
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





# # Define the home page
# @app.route('/')
# def index():
#     return render_template('index.html')


# # Define the login page
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         uname = request.form.get('uname')
#         password = request.form.get('password')    
#         this_user=User.query.filter_by(username=uname).first()
#         if this_user:
#             if check_password_hash(this_user.password, password):
#                 if this_user.type=='admin':
#                     login_user(this_user)    #Admin Authorization
#                     return redirect(url_for('admin_dash'))
#                 else:
#                     login_user(this_user)   #User Authorization
#                     return redirect(url_for('user_dash'))
#             else:
#                 return render_template('login.html', error='Invalid Password')
#         else:
#             return render_template('login.html', error='Invalid Username, Username Does Not Exist')
        
#     return render_template('login.html')


# # Define the register page
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         existing_user = User.query.filter_by(username=username).first()
#         if existing_user:
#             return render_template('register.html', error='Username already exists')
#         hashed_password = generate_password_hash(password).decode('utf-8')
#         new_user = User(name=name, username=username, email=email, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('login'))
#     return render_template('register.html')




# #Define the Search Functionality
# @app.route('/search', methods=['GET', 'POST'])
# @login_required
# def search():

#     search = request.form.get('search')
#     if not search:
#         return redirect(url_for('user_dash'))


#     books = Books.query.join(Section, Books.bs_id == Section.id).filter(or_(

#         Books.title.like(f'%{search}%'),
#         Books.author.like(f'%{search}%'),
#         Section.title.like(f'%{search}%')
            
#         )).all()
        
#     if len(books)==0:
#         return render_template('search.html', error='No books found with the given search term.',search=search)
#     if current_user.type=='admin':
#         return render_template('admin_search.html', books=books,search=search)
#     return render_template('search.html', books=books,search=search)

        
from Applications.models import User
from flask import request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from Applications.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

def role_required(role):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            if identity['type'] != role:
                return jsonify({'message': 'Access denied'}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator



def init_routes(app):
    @app.route('/login', methods=['POST'])
    def login():
        username=request.json.get('username')
        password=request.json.get('password')

        user=User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                jwt_token=create_access_token(identity={'id': user.id, 'type': user.type})
                return jsonify({'message': 'Login Successful', 'token': jwt_token, 'user_type': user.type})
            else:
                return jsonify({'message':'Invalid Password'}), 401
        else:
            return jsonify({'message':'Invalid Username'}), 401
        


    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        name=data.get('name')
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        # Check if the username or email already exists
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return jsonify({'message': 'Username or email already exists'}), 400
        
        # Hash the password
        hashed_password = generate_password_hash(password)

        user = User(name=name, username=username, password=hashed_password, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'})


    @app.route('/admin', methods=['GET'])
    @role_required('admin')
    def admin_only_route():
        return jsonify({'message': 'Welcome Admin'})

    @app.route('/user', methods=['GET'])
    @role_required('user')
    def user_only_route():
        return jsonify({'message': 'Welcome User'})