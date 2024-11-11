# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    boludeces = db.relationship('Boludez', backref='owner', lazy=True)

class Boludez(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.String(200), nullable=False)
    privacidad = db.Column(db.String(10), nullable=False)  # 'secreto', 'privado', 'publico'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)