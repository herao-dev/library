from flask import jsonify, request
from app.api import api_bp
from app.models.book import Book
from app.models.user import User
from app.models.borrow import BorrowRecord
from app.extensions import db
from app.decorators import login_required, admin_required


@api_bp.route('/books/search')
@login_required
def search_books():
    q = request.args.get('q', '', type=str)
    if len(q) < 1:
        return jsonify([])

    books = Book.query.filter(
        db.or_(Book.title.contains(q), Book.author.contains(q), Book.isbn.contains(q))
    ).limit(10).all()

    return jsonify([{
        'id': b.id,
        'title': b.title,
        'author': b.author,
        'isbn': b.isbn,
        'available_copies': b.available_copies
    } for b in books])


@api_bp.route('/users/search')
@login_required
@admin_required
def search_users():
    q = request.args.get('q', '', type=str)
    if len(q) < 1:
        return jsonify([])

    users = User.query.filter(
        db.or_(User.username.contains(q), User.email.contains(q))
    ).limit(10).all()

    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email
    } for u in users])


@api_bp.route('/borrows/stats')
@login_required
@admin_required
def borrow_stats():
    total = BorrowRecord.query.count()
    borrowed = BorrowRecord.query.filter_by(status='borrowed').count()
    overdue = BorrowRecord.query.filter_by(status='overdue').count()
    returned = BorrowRecord.query.filter_by(status='returned').count()

    return jsonify({
        'total': total,
        'borrowed': borrowed,
        'overdue': overdue,
        'returned': returned
    })
