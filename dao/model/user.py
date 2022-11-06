from setup_db import db
from marshmallow import Schema, fields


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    favourite_genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    favourite_genre = db.relationship("Genre")


class UserSchema(Schema):
    id = fields.Int()
    email = fields.String()
    password = fields.String()
    name = fields.String()
    surname = fields.String()
    favourite_genre_id = fields.Int()
