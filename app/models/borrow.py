from datetime import datetime
from app.extensions import db


class BorrowRecord(db.Model):
    __tablename__ = 'borrow_record'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    borrow_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(16), nullable=False, default='borrowed')
    fine = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    STATUS_BORROWED = 'borrowed'
    STATUS_RETURNED = 'returned'
    STATUS_OVERDUE = 'overdue'

    FINE_PER_DAY = 0.50

    @property
    def is_overdue(self):
        if self.status == self.STATUS_RETURNED:
            return False
        return datetime.utcnow() > self.due_date

    @property
    def overdue_days(self):
        if self.status == self.STATUS_RETURNED:
            if self.return_date and self.return_date > self.due_date:
                return (self.return_date - self.due_date).days
            return 0
        if datetime.utcnow() > self.due_date:
            return (datetime.utcnow() - self.due_date).days
        return 0

    def calculate_fine(self):
        return round(self.overdue_days * self.FINE_PER_DAY, 2)

    def __repr__(self):
        return f'<BorrowRecord user={self.user_id} book={self.book_id}>'