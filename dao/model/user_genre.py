from setup_db import db

user_genre = db.Table('user_movie', db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'))
                      )

