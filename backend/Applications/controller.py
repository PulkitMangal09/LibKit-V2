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

        
from Applications.models import User, Books, Section, Request, Feedback
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


    @app.route('/user', methods=['GET'])
    @jwt_required()
    def user():
        identity = get_jwt_identity()
        print(identity['type'])
        books=Books.query.all()
        all_books={}
        i=1
        for book in books:
            section=Section.query.get(book.bs_id)
            this_book={}
            this_book['id']=book.id
            this_book['title']=book.title
            this_book['author']=book.author
            this_book['content']=book.content
            this_book['image']=book.image
            this_book['bs_id']=book.bs_id
            this_book['rating']=book.rating
            this_book['section']=section.title
            all_books[f'book_{i}']=this_book
            i+=1
        return jsonify(all_books)
    
#Book Cycle Starts => Borrow Book => Pending Rquest => Approve Request => Return Book => Book Available Again

    @app.route('/userborrow/<int:id>', methods=['GET']) #Borrow Button Clicked
    @jwt_required()
    def borrow_book(id):
        user_id=get_jwt_identity()['id']
        book=Books.query.get(id)

        accepted_books_count=Request.query.filter_by(user_id=user_id, status='approved').count()
        if accepted_books_count >= 5:
            return jsonify({'message': 'You have already accepted five books. Please return a book to request another one'}), 400

        data=Request.query.all()
        if data:
            for i in data:
                if i.user_id==user_id and i.status=='pending' and i.book_id==id:
                    return jsonify({'message': 'You have already requested this book and it is pending approval. Please wait for the admin to approve your request.'}), 400
                if i.user_id==user_id and i.status=='approved' and i.book_id==id:
                    return jsonify({'message': 'You have already requested this book and it is pending return. Please return the book to request another one.'}), 400

        
        new_request=Request(user_id=user_id, book_id=id)
        db.session.add(new_request)
        db.session.commit()
        return jsonify({'message': 'Request submitted. Please wait for approval'})
      
    
    @app.route('/user_pending_requests', methods=['GET']) #show all requests
    @jwt_required()
    def pending_requests():
        user_id = get_jwt_identity()['id']
        requests = Request.query.filter_by(user_id=user_id).all()
        all_requests = []
        for request in requests:
            book = Books.query.get(request.book_id)
            section = Section.query.get(book.bs_id)
            this_request = {
                'id': request.id,
                'status': request.status,
                'book_title': book.title,
                'book_author': book.author,
                'section': section.title
            }
            all_requests.append(this_request)
        return jsonify(all_requests)

    

    @app.route('/admin_pending_requests', methods=['GET']) #Admin Dashboard Pending Page shows all the pending requests
    @role_required('admin')
    def admin_pending_request():
        requests=Request.query.filter_by(status='pending').all()
        all_requests={}
        i=1
        for request in requests:
            user=User.query.get(request.user_id)
            book=Books.query.get(request.book_id)
            section=Section.query.get(book.bs_id)
            this_request={}
            this_request['id']=request.id
            this_request['status']=request.status
            this_request['user_name']=user.name
            this_request['book_title']=book.title
            this_request['book_author']=book.author
            this_request['section']=section.title
            all_requests[f'request_{i}']=this_request
            i+=1
        return jsonify(all_requests)
    

    @app.route('/admin_approve/<int:id>', methods=['GET']) #Admin Dashboard Approve Button Clicked
    @role_required('admin')
    def admin_approve_button(id):

        request=Request.query.get(id)
        user_id=request.user_id
        #Check if user has already accepted 5 books
        accepted_books_count=Request.query.filter_by(user_id=user_id, status='approved').count()
        if accepted_books_count >= 5:
            return jsonify({'message': 'User has already accepted five books. Cannot approve new request.'}), 400

        new_feedback=Feedback(borrow_user_id=user_id, book_id=request.book_id)
        db.session.add(new_feedback)

        request.status='approved'
        db.session.commit()
        return jsonify({'message': 'Request approved successfully'})
    

    @app.route('/admin_reject/<int:id>', methods=['GET']) #Admin Reject Button Clicked
    @role_required('admin')
    def admin_reject(id):
        request=Request.query.get(id)
        request.status='rejected'
        db.session.commit()
        return jsonify({'message': 'Request rejected successfully'})


    @app.route('/user_approved_books', methods=['GET'])
    @jwt_required()
    def approved_requests():
        user_id = get_jwt_identity()['id']
        requests = Request.query.filter_by(user_id=user_id, status='approved').all()
        all_requests = []
        for request in requests:
            book = Books.query.get(request.book_id)
            section = Section.query.get(book.bs_id)
            this_request = {
                'id': request.id,
                'title': book.title,
                'author': book.author,
                'content': book.content,
                'section': section.title,
                'image': book.image  # Assuming you have this field
            }
            all_requests.append(this_request)
        return jsonify(all_requests)

    

    @app.route('/return_book/<int:id>', methods=['GET']) #Return Button Clicked
    @jwt_required()
    def return_book(id):

        request=Request.query.get(id)
        feedback=Feedback.query.filter_by(book_id=request.book_id , borrow_user_id=get_jwt_identity()['id']).first()
        feedback.phase='returned'
        request.status='return'
        db.session.delete(request)
        db.session.commit()
        return jsonify({'message': 'Book returned successfully'})  #User will go to feedback page after returning the book
    

    

    @app.route('/admin_approve_books', methods=['GET']) #Admin Dashboard Approved Book View
    @role_required('admin')
    def admin_approve_books():
        requests=Request.query.filter_by(status='approved').all()
        all_requests=[]
        for request in requests:
            user=User.query.get(request.user_id)
            book=Books.query.get(request.book_id)
            section=Section.query.get(book.bs_id)
            this_request={
            'id':request.id,
            'user_id':request.user_id,
            'status':request.status,
            'user_name':user.name,
            'book_title':book.title,
            'book_author':book.author,
            'section':section.title
          
            }
            all_requests.append(this_request)

        return jsonify(all_requests)
    

    @app.route('/admin_rejected_books', methods=['GET']) #Admin Dash Rejected Books View
    @role_required('admin')
    def admin_rejected_books():
        requests=Request.query.filter_by(status='rejected').all()
        all_requests={}
        i=1
        for request in requests:
            user=User.query.get(request.user_id)
            book=Books.query.get(request.book_id)
            section=Section.query.get(book.bs_id)
            this_request={}
            this_request['id']=request.id
            this_request['status']=request.status
            this_request['user_name']=user.name
            this_request['book_title']=book.title
            this_request['book_author']=book.author
            this_request['section']=section.title
            all_requests[f'request_{i}']=this_request
            i+=1
        return jsonify(all_requests)
    
    @app.route('/revoke/<int:id>', methods=['GET']) #Revoke Button Clicked
    @role_required('admin')
    def revoke(id):
        request=Request.query.get(id)
        feedback=Feedback.query.filter_by(book_id=request.book_id, borrow_user_id=request.user_id).first()
        feedback.phase='revoked'
        request.status='returned'
        db.session.commit()
        return jsonify({'message': 'Request revoked successfully'})