from app import db
from datetime import datetime
from flask_login import UserMixin

class RegistroAgua(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, default=datetime.utcnow)
    captada = db.Column(db.Float, nullable=False)
    consumida = db.Column(db.Float, nullable=False)
    observaciones = db.Column(db.String(200))

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    correo = db.Column(db.String(100), unique=True)
    contraseña = db.Column(db.String(100))
