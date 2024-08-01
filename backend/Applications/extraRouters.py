from Applications.models import *
from Applications.controller import *
from flask import request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from Applications.database import db
from functools import wraps
from Applications.config import cache
import datetime
from Applications.tasks import export_books_cycle_to_csv





def er_init_routes(app):

    @app.route('/cache')
    @cache.cached(timeout=50)
    def get_cached_time():
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return jsonify({'cached_time': current_time})
    
    @app.route('/top_books', methods=['GET'])
    def top_books():
        books = Books.query.order_by(Books.rating.desc()).limit(1).all()
        top_books = []
        for book in books:
            this_book = {}
            this_book['id'] = book.id
            this_book['title'] = book.title
            this_book['author'] = book.author
            this_book['content'] = book.content
            this_book['image'] = book.image
            this_book['rating'] = book.rating
            top_books.append(this_book)
        return jsonify(top_books)

    @app.route('/<int:id>/issued_users', methods=['GET'])
    @role_required('admin')
    def issued_users(id):
        issued_books = Request.query.filter_by(book_id=id,status='approved').all()
        users = []

        for book in issued_books:
            user = User.query.filter_by(id=book.user_id).first()
            this_user = {}
            this_user['request_id'] = book.id
            this_user['id'] = user.id
            this_user['name'] = user.name
            this_user['username'] = user.username
            this_user['email'] = user.email
            users.append(this_user)
        return jsonify(users)
    

    #This route will triger the task to export the request data to csv file
    @app.route('/export_request', methods=['GET'])
    @role_required('admin')
    def export_request():
        export_books_cycle_to_csv.delay()
        return jsonify({'message': 'Request data is being exported to CSV file. You will receive an email shortly.'})
        

    @app.route('/book_cycle') #making route for above job
    def book_cycle():
        request=Request.query.all()
        book_cycle=[]
        for req in request:

            user=User.query.filter_by(id=req.user_id).first()
            book=Books.query.filter_by(id=req.book_id).first()
            section=Section.query.filter_by(id=book.bs_id).first()
            this_cycle={}
            this_cycle['user']=user.name
            this_cycle['book']=book.title
            this_cycle['author']=book.author
            this_cycle['section']=section.title
            this_cycle['issued_date']=req.issued_date
            this_cycle['return_date']=req.return_date
            book_cycle.append(this_cycle)
        return jsonify(book_cycle)
    

    #This route will triger to check whether the user has visited or not
    @app.route('/visited', methods=['GET'])
    def visited():
        user=User.query.all()
        current_date=datetime.datetime.now().strftime("%B %d, %Y")
        user_visited=[]
        for user in user:
            if user.id!=1:
                if user.last_login!=current_date:
                    dict={}
                    dict['id']=user.id
                    dict['username']=user.username
                    dict['name']=user.name
                    dict['email']=user.email
                    user_visited.append(dict)
        return jsonify(user_visited)
    
    #this router will create the monthly report
    @app.route('/monthly_report', methods=['GET'])
    def monthly_report():
        number_of_sections=Section.query.count()
        number_of_books=Books.query.count()
        number_of_users=User.query.count()
        number_of_books_issued=Request.query.filter_by(status='approved').count()
        temp=Books.query.all()

        books=[]
        for book in temp:
            dict={}
            if book.rating:
                rating=book.rating
                dict['id']=book.id
                dict['title']=book.title
                dict['author']=book.author
                dict['rating']=rating
            else:
                dict['id']=book.id
                dict['title']=book.title
                dict['author']=book.author
                dict['rating']=0
            books.append(dict)
        
        report={}
        report['number_of_sections']=number_of_sections
        report['number_of_books']=number_of_books
        report['number_of_users']=number_of_users
        report['number_of_books_issued']=number_of_books_issued
        report['books']=books
        return jsonify(report)




