from datetime import datetime
from app.extensions import db


class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    reserve_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(16), nullable=False, default='pending')
    notify_date = db.Column(db.DateTime, nullable=True)
    expire_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    STATUS_PENDING = 'pending'
    STATUS_FULFILLED = 'fulfilled'
    STATUS_CANCELLED = 'cancelled'
    STATUS_EXPIRED = 'expired'

    user = db.relationship('User', backref=db.backref('reservations', lazy='dynamic'))
    book = db.relationship('Book', backref=db.backref('reservations', lazy='dynamic'))

    def __repr__(self):
        return f'<Reservation user={self.user_id} book={self.book_id}>'