from datetime import datetime
from app.extensions import db


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256), nullable=False)
    author = db.Column(db.String(128), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=True)
    publisher = db.Column(db.String(128), nullable=True)
    publish_date = db.Column(db.Date, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='SET NULL'), nullable=True)
    total_copies = db.Column(db.Integer, nullable=False, default=1)
    available_copies = db.Column(db.Integer, nullable=False, default=1)
    cover_image = db.Column(db.String(256), nullable=True)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    borrow_records = db.relationship('BorrowRecord', backref='book', lazy='dynamic')

    @property
    def is_available(self):
        return self.available_copies > 0

    def __repr__(self):
        return f'<Book {self.title}>'