from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
import base64,sqlalchemy 
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin

db = SQLAlchemy()


roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
    db.PrimaryKeyConstraint('user_id', 'role_id')
)



class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    last_login = db.Column(db.DateTime)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('user', lazy='dynamic'))



class BookCategory(db.Model):
    __tablename__ = 'book_category'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    category = db.Column(db.String(40), unique=True, nullable=False)
    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category
        }

class BookDetails(db.Model):
    __tablename__ = 'book_details'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    category = db.Column(db.String(40), db.ForeignKey('book_category.category'))
    pdf = db.Column(db.BLOB)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'category': self.category,
            'pdf': self.get_pdf_data() 
        }
        
    def get_pdf_data(self):
        if self.pdf:
            # Convert BLOB to Base64-encoded string
            return base64.b64encode(self.pdf).decode('utf-8')
        else:
            return None
        ''



class BookRating(db.Model):
    __tablename__ = 'book_rating'

    book_id = db.Column(db.Integer, db.ForeignKey('book_details.id'), primary_key=True)
    username = db.Column(db.String(40), db.ForeignKey('users.username'), primary_key=True)
    rating = db.Column(db.Integer)
    review = db.Column(db.Text)
    
    

class BookRequests(db.Model):
    __tablename__ = 'book_requests'

    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), db.ForeignKey('users.username'))
    book_id = db.Column(db.Integer, db.ForeignKey('book_details.id'))
    status = db.Column(db.String(20), CheckConstraint("status IN ('pending', 'approved', 'rejected')"), default='pending', nullable=False)
    issue_date = db.Column(db.Date, server_default=db.func.current_date(), nullable=False)
    return_date = db.Column(db.Date)
    request_date = db.Column(db.Date, server_default=db.func.current_date())  # Adjusted default value
    duration = db.Column(db.Integer, default=None)  # Added duration column with default None
    
    
    
    book = db.relationship('BookDetails', backref='requests', lazy=True)
    
    
    
    def __init__(self, username, book_id, status='pending', issue_date=None, return_date=None, duration=None):
        self.username = username   
        self.book_id = book_id
        self.status = status
        self.issue_date = issue_date
        self.return_date = return_date
        self.duration = duration
    def to_dict(self):
            return {
            'request_id': self.request_id,
            'username': self.username,
            'book_id': self.book_id,
            'book_title': self.book.title if self.book else None,
            'book_author': self.book.title if self.book else None,
            'book_category': self.book.title if self.book else None,

            'status': self.status,
            'status': self.status,
            'issue_date': self.issue_date.strftime('%Y-%m-%d') if self.issue_date else None,
            'return_date': self.return_date.strftime('%Y-%m-%d') if self.return_date else None,
            'request_date': self.request_date.strftime('%Y-%m-%d'),
            'duration': self.duration
        }        

    
class BookReviews(db.Model):
    __tablename__ = 'book_reviews'

    book_id = db.Column(db.Integer, db.ForeignKey('book_details.id'), primary_key=True)
    username = db.Column(db.String(40), db.ForeignKey('users.username'), primary_key=True)
    review = db.Column(db.Text)
