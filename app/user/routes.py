from datetime import datetime
from flask import request, jsonify
from flask_jwt_extended import get_current_user
from app.user import user_bp
from app.models.book import Book
from app.models.category import Category
from app.models.borrow import BorrowRecord
from app.models.reservation import Reservation
from app.models.review import Review
from app.models.announcement import Announcement
from app.extensions import db
from app.decorators import login_required
from app.utils import get_due_date, update_overdue_status


def book_to_dict(b):
    return {
        'id': b.id, 'title': b.title, 'author': b.author,
        'isbn': b.isbn, 'publisher': b.publisher,
        'publish_date': b.publish_date.isoformat() if b.publish_date else None,
        'category': b.category.name if b.category else None,
        'total_copies': b.total_copies, 'available_copies': b.available_copies,
        'cover_image': b.cover_image, 'description': b.description,
        'location': b.location, 'is_available': b.is_available,
    }


def borrow_serializer(r):
    return {
        'id': r.id, 'book_id': r.book_id,
        'book': r.book.title, 'author': r.book.author,
        'borrow_date': r.borrow_date.isoformat(),
        'due_date': r.due_date.isoformat(),
        'return_date': r.return_date.isoformat() if r.return_date else None,
        'status': r.status, 'fine': float(r.fine),
        'is_overdue': r.is_overdue,
    }


def reservation_serializer(r):
    return {
        'id': r.id, 'book_id': r.book_id,
        'book': r.book.title, 'author': r.book.author,
        'reserve_date': r.reserve_date.isoformat(), 'status': r.status,
    }


# --- Dashboard ---
@user_bp.route('/dashboard')
@login_required
def dashboard():
    user = get_current_user()
    update_overdue_status()
    borrowed_count = BorrowRecord.query.filter_by(user_id=user.id).filter(
        BorrowRecord.status.in_(['borrowed', 'overdue'])
    ).count()
    overdue_count = BorrowRecord.query.filter_by(user_id=user.id, status='overdue').count()
    total_borrowed = BorrowRecord.query.filter_by(user_id=user.id).count()
    recent_borrows = BorrowRecord.query.filter_by(user_id=user.id).order_by(
        BorrowRecord.created_at.desc()
    ).limit(5).all()
    recent_books = Book.query.order_by(Book.created_at.desc()).limit(6).all()
    announcements = Announcement.query.filter_by(is_published=True).order_by(
        Announcement.created_at.desc()
    ).limit(3).all()

    return jsonify({
        "success": True,
        "data": {
            "borrowed_count": borrowed_count,
            "overdue_count": overdue_count,
            "total_borrowed": total_borrowed,
            "recent_borrows": [borrow_serializer(r) for r in recent_borrows],
            "recent_books": [book_to_dict(b) for b in recent_books],
            "announcements": [{
                'id': a.id, 'title': a.title, 'content': a.content,
                'priority': a.priority,
                'created_at': a.created_at.isoformat() if a.created_at else None,
            } for a in announcements],
        }
    })


# --- Book Browsing ---
@user_bp.route('/books')
@login_required
def book_list():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    category_id = request.args.get('category_id', 0, type=int)

    query = Book.query
    if search:
        query = query.filter(
            db.or_(Book.title.contains(search), Book.author.contains(search))
        )
    if category_id > 0:
        query = query.filter_by(category_id=category_id)

    query = query.order_by(Book.updated_at.desc())
    pagination = query.paginate(page=page, per_page=12, error_out=False)
    categories = Category.query.order_by(Category.name).all()

    return jsonify({
        "success": True,
        "data": [book_to_dict(b) for b in pagination.items],
        "pagination": {
            "page": pagination.page, "per_page": pagination.per_page,
            "total": pagination.total, "pages": pagination.pages,
        },
        "categories": [{'id': c.id, 'name': c.name} for c in categories],
    })


@user_bp.route('/books/<int:book_id>')
@login_required
def book_detail(book_id):
    user = get_current_user()
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"success": False, "message": "图书不存在"}), 404

    my_borrow = BorrowRecord.query.filter_by(user_id=user.id, book_id=book_id).filter(
        BorrowRecord.status.in_(['borrowed', 'overdue'])
    ).first()

    my_reservation = Reservation.query.filter_by(user_id=user.id, book_id=book_id).filter(
        Reservation.status.in_(['pending'])
    ).first()

    reviews = Review.query.filter_by(book_id=book_id, is_visible=True).order_by(Review.created_at.desc()).all()
    avg_rating = db.session.query(db.func.avg(Review.rating)).filter_by(book_id=book_id, is_visible=True).scalar()
    avg_rating = round(avg_rating, 1) if avg_rating else 0

    has_borrowed = BorrowRecord.query.filter_by(user_id=user.id, book_id=book_id).first() is not None
    my_review = Review.query.filter_by(user_id=user.id, book_id=book_id).first()

    return jsonify({
        "success": True,
        "data": {
            "book": book_to_dict(book),
            "my_borrow": None if not my_borrow else {
                'id': my_borrow.id, 'status': my_borrow.status,
                'borrow_date': my_borrow.borrow_date.isoformat(),
                'due_date': my_borrow.due_date.isoformat(),
            },
            "my_reservation": None if not my_reservation else {
                'id': my_reservation.id, 'status': my_reservation.status,
            },
            "has_borrowed": has_borrowed,
            "my_review": None if not my_review else {
                'id': my_review.id, 'rating': my_review.rating,
                'content': my_review.content,
            },
            "reviews": [{
                'id': r.id, 'user': r.user.username, 'rating': r.rating,
                'content': r.content,
                'created_at': r.created_at.isoformat() if r.created_at else None,
            } for r in reviews],
            "avg_rating": avg_rating,
        }
    })


# --- Borrow Actions ---
@user_bp.route('/books/<int:book_id>/borrow', methods=['POST'])
@login_required
def book_borrow(book_id):
    user = get_current_user()
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"success": False, "message": "图书不存在"}), 404
    if book.available_copies <= 0:
        return jsonify({"success": False, "message": "该图书库存不足，无法借阅"}), 400

    existing = BorrowRecord.query.filter_by(user_id=user.id, book_id=book_id).filter(
        BorrowRecord.status.in_(['borrowed', 'overdue'])
    ).first()
    if existing:
        return jsonify({"success": False, "message": "您已经借阅了该图书，请先归还后再借"}), 400

    record = BorrowRecord(
        user_id=user.id, book_id=book_id,
        borrow_date=datetime.utcnow(), due_date=get_due_date(),
        status=BorrowRecord.STATUS_BORROWED
    )
    book.available_copies -= 1
    db.session.add(record)
    db.session.commit()
    return jsonify({"success": True, "message": "借阅成功！请在规定时间内归还"})


@user_bp.route('/borrows')
@login_required
def borrow_list():
    user = get_current_user()
    update_overdue_status()
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '', type=str)

    query = BorrowRecord.query.filter_by(user_id=user.id)
    if status_filter:
        query = query.filter_by(status=status_filter)

    query = query.order_by(BorrowRecord.created_at.desc())
    pagination = query.paginate(page=page, per_page=10, error_out=False)

    return jsonify({
        "success": True,
        "data": [borrow_serializer(r) for r in pagination.items],
        "pagination": {
            "page": pagination.page, "per_page": pagination.per_page,
            "total": pagination.total, "pages": pagination.pages,
        }
    })


@user_bp.route('/borrows/<int:record_id>/return', methods=['POST'])
@login_required
def borrow_return(record_id):
    user = get_current_user()
    record = db.session.get(BorrowRecord, record_id)
    if not record or record.user_id != user.id:
        return jsonify({"success": False, "message": "借阅记录不存在"}), 404
    if record.status == BorrowRecord.STATUS_RETURNED:
        return jsonify({"success": False, "message": "该记录已归还"}), 400

    record.return_date = datetime.utcnow()
    record.status = BorrowRecord.STATUS_RETURNED
    record.fine = record.calculate_fine()
    record.book.available_copies += 1
    db.session.commit()

    msg = f"还书成功！逾期 {record.overdue_days} 天，罚金 ¥{record.fine:.2f}" if record.fine > 0 else "还书成功"
    return jsonify({"success": True, "message": msg})


# --- Reservations ---
@user_bp.route('/books/<int:book_id>/reserve', methods=['POST'])
@login_required
def book_reserve(book_id):
    user = get_current_user()
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"success": False, "message": "图书不存在"}), 404
    if book.available_copies > 0:
        return jsonify({"success": False, "message": "该图书还有库存，请直接借阅"}), 400

    existing = Reservation.query.filter_by(user_id=user.id, book_id=book_id, status='pending').first()
    if existing:
        return jsonify({"success": False, "message": "您已经预约了该图书，请耐心等待"}), 400

    reservation = Reservation(user_id=user.id, book_id=book_id, status=Reservation.STATUS_PENDING)
    db.session.add(reservation)
    db.session.commit()
    return jsonify({"success": True, "message": "预约成功！图书可借时会通知您"})


@user_bp.route('/reservations')
@login_required
def reservation_list():
    user = get_current_user()
    page = request.args.get('page', 1, type=int)
    query = Reservation.query.filter_by(user_id=user.id).order_by(Reservation.created_at.desc())
    pagination = query.paginate(page=page, per_page=10, error_out=False)

    return jsonify({
        "success": True,
        "data": [reservation_serializer(r) for r in pagination.items],
        "pagination": {
            "page": pagination.page, "per_page": pagination.per_page,
            "total": pagination.total, "pages": pagination.pages,
        }
    })


@user_bp.route('/reservations/<int:reservation_id>/cancel', methods=['POST'])
@login_required
def reservation_cancel(reservation_id):
    user = get_current_user()
    reservation = db.session.get(Reservation, reservation_id)
    if not reservation or reservation.user_id != user.id:
        return jsonify({"success": False, "message": "预约记录不存在"}), 404

    reservation.status = Reservation.STATUS_CANCELLED
    db.session.commit()
    return jsonify({"success": True, "message": "预约已取消"})


# --- Reviews ---
@user_bp.route('/books/<int:book_id>/review', methods=['POST'])
@login_required
def book_review(book_id):
    user = get_current_user()
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"success": False, "message": "图书不存在"}), 404

    has_borrowed = BorrowRecord.query.filter_by(user_id=user.id, book_id=book_id).first()
    if not has_borrowed:
        return jsonify({"success": False, "message": "您需要借阅过该图书才能发表评论"}), 400

    data = request.get_json()
    rating = int(data.get('rating', 5))
    content = data.get('content', '').strip()

    existing = Review.query.filter_by(user_id=user.id, book_id=book_id).first()
    if existing:
        existing.rating = rating
        existing.content = content
        db.session.commit()
        return jsonify({"success": True, "message": "评论已更新"})
    else:
        review = Review(user_id=user.id, book_id=book_id, rating=rating, content=content)
        db.session.add(review)
        db.session.commit()
        return jsonify({"success": True, "message": "评论发表成功"})


# --- Profile ---
@user_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    user = get_current_user()
    return jsonify({"success": True, "data": user.to_dict()})


@user_bp.route('/profile', methods=['PUT'])
@login_required
def profile_update():
    user = get_current_user()
    data = request.get_json()

    username = data.get('username', '').strip()
    email = data.get('email', '').strip()

    if username:
        existing = User.query.filter_by(username=username).first()
        if existing and existing.id != user.id:
            return jsonify({"success": False, "message": "该用户名已存在"}), 400
        user.username = username
    if email:
        existing = User.query.filter_by(email=email).first()
        if existing and existing.id != user.id:
            return jsonify({"success": False, "message": "该邮箱已存在"}), 400
        user.email = email

    user.phone = data.get('phone', '').strip() or None
    db.session.commit()
    return jsonify({"success": True, "message": "个人信息更新成功", "data": user.to_dict()})


@user_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    user = get_current_user()
    data = request.get_json()

    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')
    confirm_password = data.get('confirm_password', '')

    if not user.check_password(old_password):
        return jsonify({"success": False, "message": "当前密码错误"}), 400
    if len(new_password) < 6:
        return jsonify({"success": False, "message": "密码长度不能少于6位"}), 400
    if new_password != confirm_password:
        return jsonify({"success": False, "message": "两次密码输入不一致"}), 400

    user.set_password(new_password)
    db.session.commit()
    return jsonify({"success": True, "message": "密码修改成功"})


# Need to import User model for the profile validation
from app.models.user import User
