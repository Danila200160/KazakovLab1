from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Page(db.Model):
    __tablename__ = 'pages'  # Явно указываем имя таблицы
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    content = db.Column(db.Text)
    
    

class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Явно указываем имя таблицы
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    