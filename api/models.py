from datetime import datetime
from .extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    attempted_at = db.Column(db.DateTime, nullable=True)
    attempt = db.Column(db.Integer, default=0)
