from datetime import datetime
from app.extensions import db


class Announcement(db.Model):
    __tablename__ = 'announcement'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(16), nullable=False, default='normal')
    is_published = db.Column(db.Boolean, nullable=False, default=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    PRIORITY_NORMAL = 'normal'
    PRIORITY_IMPORTANT = 'important'
    PRIORITY_URGENT = 'urgent'

    publisher = db.relationship('User', backref=db.backref('announcements', lazy='dynamic'))

    def __repr__(self):
        return f'<Announcement {self.title}>'