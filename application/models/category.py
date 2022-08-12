from application import db
from sqlalchemy import func

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(128))
    date_added = db.Column(db.DateTime, default=func.now())

    user = db.relationship('User', backref='category', lazy=True)

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)
