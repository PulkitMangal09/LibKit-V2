from flask_restful import Api, Resource,reqparse
from Applications.models import *
from Applications.controller import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from Applications.controller import init_routes
import datetime

api=Api() # Equivalent to write api = Api(app) in app.py


# Section API parser
section_parser = reqparse.RequestParser()
section_parser.add_argument('title', type=str, required=True, help="Title is required")
section_parser.add_argument('image', type=str, required=True, help="Image is required")
section_parser.add_argument('description', type=str, required=True, help="Description is required")

# Book API parser
book_parser = reqparse.RequestParser()
book_parser.add_argument('title', type=str, required=True, help="Title is required")
book_parser.add_argument('author', type=str, required=True, help="Author is required")
book_parser.add_argument('content', type=str, required=True, help="Content is required")
book_parser.add_argument('image', type=str, required=True, help="Image is required")
book_parser.add_argument('rating', type=int)

class SectionAPI(Resource):

    @role_required('admin')

    def get(self): # post, put, delete
        sections = Section.query.all()
        all_sections = {}
        i=1
        for section in sections:
            this_section = {}
            this_section['id'] = section.id
            this_section['title'] = section.title
            this_section['date'] = section.date
            this_section['image'] = section.image
            this_section['description'] = section.description
            all_sections[f'section_{i}'] = this_section
            i+=1
        return all_sections
        
    @role_required('admin')
    def post(self):
        args = section_parser.parse_args()
        if not args['title'] or not args['image'] or not args['description']:
            return {'message': 'All fields are required'}, 400
        elif Section.query.filter_by(title=args['title']).first():
            return {'message': 'Section already exists'}, 400
        else:
            temp = datetime.datetime.now()
            formatted_date = temp.strftime("%B %d, %Y")
            section = Section(title=args['title'], date=formatted_date, image=args['image'], description=args['description'])
            db.session.add(section)
            db.session.commit()
            return {'message': 'Section added successfully'}, 201
        
    @role_required('admin')
    def put(self, id):
        args = section_parser.parse_args()
        section = Section.query.filter_by(id=id).first()
        if not args['title'] or not args['image'] or not args['description']:
            return {'message': 'All fields are required'}, 400
        
        if not section:
            return {'message': 'Section not found'}, 404
        else:
            section.title = args['title']
            temp = datetime.datetime.now()
            section.date = temp.strftime("%B %d, %Y")
            section.image = args['image']
            section.description = args['description']
            db.session.commit()
            return {'message': 'Section updated successfully'}, 200
        
    
    @role_required('admin')
    def delete(self, id):
        section = Section.query.filter_by(id=id).first()
        if not section:
            return {'message': 'Section not found'}, 404
        else:
            db.session.delete(section)
            db.session.commit()
            return {'message': 'Section deleted successfully'}, 200



        

api.add_resource(SectionAPI, '/api/all_sections', '/api/create_section', '/api/<int:id>/update_section', '/api/<int:id>/delete_section' ) # Equivalent to write api.add_resource(SesctionAPI, '/sections', app=app) in app.py



class BookAPI(Resource):


    @role_required('admin')
    def get(self,id):
        books = Books.query.filter_by(bs_id=id).all()
        all_books = {}
        i=1
        for book in books:
            this_book = {}
            this_book['id'] = book.id
            this_book['title'] = book.title
            this_book['author'] = book.author
            this_book['content'] = book.content
            this_book['image'] = book.image
            this_book['bs_id'] = book.bs_id
            this_book['rating'] = book.rating
            all_books[f'book_{i}'] = this_book
            i+=1
        return all_books
    
    @role_required('admin')
    def post(self,id):
        args = book_parser.parse_args()
        if not args['title'] or not args['author'] or not args['content'] or not args['image']:
            return {'message': 'All fields are required'}, 400
        elif Books.query.filter_by(title=args['title']).first():
            return {'message': 'Book already exists'}, 400
        else:
            book = Books(title=args['title'], author=args['author'], content=args['content'], image=args['image'], bs_id=id, rating=args['rating'])
            db.session.add(book)
            db.session.commit()
            return {'message': 'Book added successfully'}, 201
        

    @role_required('admin')
    def put(self, id):
        args = book_parser.parse_args()
        book = Books.query.filter_by(id=id).first()
        section_id=book.bs_id
        if not args['title'] or not args['author'] or not args['content'] or not args['image'] :
            return {'message': 'All fields are required'}, 400
        
        if not book:
            return {'message': 'Book not found'}, 404
        else:
            book.title = args['title']
            book.author = args['author']
            book.content = args['content']
            book.image = args['image']
            db.session.commit()
            return {'message': 'Book updated successfully','section_id': section_id}, 200
        

    @role_required('admin')
    def delete(self, id):
        book = Books.query.filter_by(id=id).first()
        if not book:
            return {'message': 'Book not found'}, 404
        else:
            db.session.delete(book)
            db.session.commit()
            return {'message': 'Book deleted successfully'}, 200





api.add_resource(BookAPI, '/api/<int:id>/all_books','/api/<int:id>/add_book','/api/<int:id>/update_book','/api/<int:id>/delete_book') # Equivalent to write api.add_resource(SesctionAPI, '/sections', app=app) in app.py



# Function to initialize the app

def init_app(app):
    api.init_app(app) # Equivalent to write api = Api(app) in app.py
    init_routes(app) # Equivalent to write from Applications.controller import init_routes in app.py