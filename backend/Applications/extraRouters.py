from Applications.models import *
from Applications.controller import *
from flask import request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from Applications.database import db
from functools import wraps
from Applications.config import cache
import datetime


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