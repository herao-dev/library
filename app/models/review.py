from datetime import datetime
from app.extensions import db


class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=5)
    content = db.Column(db.Text, nullable=True)
    is_visible = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('reviews', lazy='dynamic'))
    book = db.relationship('Book', backref=db.backref('reviews', lazy='dynamic'))

    def __repr__(self):
        return f'<Review user={self.user_id} book={self.book_id} rating={self.rating}>'