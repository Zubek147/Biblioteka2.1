from flask_sqlalchemy import SQLAlchemy
from app import db
from sqlalchemy import Boolean

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    year = db.Column(db.Integer)
    genre = db.Column(db.String(64))
    description = db.Column(db.Text)
    loaned = db.Column(Boolean,default=False)
    owned = db.Column(Boolean, default=False)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    birth_date = db.Column(db.String(10)) 
    nationality = db.Column(db.String(64))
    books = db.relationship('Book', backref='author', lazy=True)
