from application import db
from sqlalchemy import func

class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(128))
    date_added = db.Column(db.DateTime, default=func.now())

    user = db.relationship('User', backref='genre', lazy=True)

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)
