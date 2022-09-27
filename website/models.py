from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(150))
    StudentID = db.Column(db.String(150))
    group = db.Column(db.Integer)
    idx_csv=db.Column(db.Integer)
    # notes = db.relationship('Note')
