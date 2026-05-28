from datetime import datetime
from flask import request, jsonify
from flask_jwt_extended import get_current_user
from app.admin import admin_bp
from app.models.book import Book
from app.models.category import Category
from app.models.user import User
from app.models.borrow import BorrowRecord
from app.models.reservation import Reservation
from app.models.review import Review
from app.models.announcement import Announcement
from app.extensions import db
from app.decorators import admin_required
from app.utils import save_upload_file, get_due_date, update_overdue_status


def paginated_response(query, page, per_page=10, serializer=None):
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    items = pagination.items
    if serializer:
        data = [serializer(item) for item in items]
    else:
        data = [item.to_dict() if hasattr(item, 'to_dict') else item for item in items]
    return {
        "success": True,
        "data": data,
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
        }
    }


# --- Dashboard ---
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    update_overdue_status()
    total_books = Book.query.count()
    total_users = User.query.count()
    borrowed_count = BorrowRecord.query.filter(BorrowRecord.status.in_(['borrowed', 'overdue'])).count()
    overdue_count = BorrowRecord.query.filter_by(status='overdue').count()
    total_categories = Category.query.count()
    total_reservations = Reservation.query.filter_by(status='pending').count()
    total_reviews = Review.query.count()
    total_fines = float(db.session.query(db.func.sum(BorrowRecord.fine)).scalar() or 0)

    recent_borrows = BorrowRecord.query.order_by(BorrowRecord.created_at.desc()).limit(10).all()
    recent_reviews = Review.query.filter_by(is_visible=True).order_by(Review.created_at.desc()).limit(5).all()
    latest_announcements = Announcement.query.filter_by(is_published=True).order_by(Announcement.created_at.desc()).limit(5).all()

    def borrow_serializer(r):
        return {
            'id': r.id, 'user': r.user.username, 'book': r.book.title,
            'status': r.status, 'borrow_date': r.borrow_date.isoformat(),
            'due_date': r.due_date.isoformat(),
            'return_date': r.return_date.isoformat() if r.return_date else None,
            'fine': float(r.fine),
        }

    def review_serializer(rv):
        return {
            'id': rv.id, 'user': rv.user.username, 'book': rv.book.title,
            'rating': rv.rating, 'content': rv.content,
            'created_at': rv.created_at.isoformat() if rv.created_at else None,
        }

    def announcement_serializer(a):
        return {
            'id': a.id, 'title': a.title, 'priority': a.priority,
            'created_at': a.created_at.isoformat() if a.created_at else None,
        }

    return jsonify({
        "success": True,
        "data": {
            "total_books": total_books, "total_users": total_users,
            "borrowed_count": borrowed_count, "overdue_count": overdue_count,
            "total_categories": total_categories, "total_reservations": total_reservations,
            "total_reviews": total_reviews, "total_fines": total_fines,
            "recent_borrows": [borrow_serializer(r) for r in recent_borrows],
            "recent_reviews": [review_serializer(r) for r in recent_reviews],
            "latest_announcements": [announcement_serializer(a) for a in latest_announcements],
        }
    })


# --- Book CRUD ---
def book_to_dict(b):
    return {
        'id': b.id, 'title': b.title, 'author': b.author,
        'isbn': b.isbn, 'publisher': b.publisher,
        'publish_date': b.publish_date.isoformat() if b.publish_date else None,
        'category_id': b.category_id, 'category': b.category.name if b.category else None,
        'total_copies': b.total_copies, 'available_copies': b.available_copies,
        'cover_image': b.cover_image, 'description': b.description,
        'location': b.location, 'is_available': b.is_available,
        'created_at': b.created_at.isoformat() if b.created_at else None,
    }


@admin_bp.route('/books')
@admin_required
def book_list():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    category_id = request.args.get('category_id', 0, type=int)

    query = Book.query
    if search:
        query = query.filter(
            db.or_(Book.title.contains(search), Book.author.contains(search), Book.isbn.contains(search))
        )
    if category_id > 0:
        query = query.filter_by(category_id=category_id)

    query = query.order_by(Book.updated_at.desc())
    return jsonify(paginated_response(query, page, 10, book_to_dict))


@admin_bp.route('/books', methods=['POST'])
@admin_required
def book_add():
    title = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    if not title or not author:
        return jsonify({"success": False, "message": "书名和作者不能为空"}), 400

    isbn = request.form.get('isbn', '').strip() or None
    if isbn:
        existing = Book.query.filter_by(isbn=isbn).first()
        if existing:
            return jsonify({"success": False, "message": "该ISBN已存在"}), 400

    try:
        total_copies = int(request.form.get('total_copies', 1))
        available_copies = int(request.form.get('available_copies', total_copies))
    except ValueError:
        return jsonify({"success": False, "message": "册数参数无效"}), 400

    category_id = request.form.get('category_id', type=int)
    if category_id and category_id <= 0:
        category_id = None

    book = Book(
        title=title, author=author, isbn=isbn,
        publisher=request.form.get('publisher', '').strip() or None,
        publish_date=datetime.strptime(request.form.get('publish_date'), '%Y-%m-%d').date() if request.form.get('publish_date') else None,
        category_id=category_id,
        total_copies=total_copies, available_copies=available_copies,
        description=request.form.get('description', '').strip() or None,
        location=request.form.get('location', '').strip() or None,
    )

    cover = request.files.get('cover_image')
    if cover and cover.filename:
        book.cover_image = save_upload_file(cover)

    db.session.add(book)
    db.session.commit()
    return jsonify({"success": True, "message": "图书添加成功", "data": book_to_dict(book)})


@admin_bp.route('/books/<int:book_id>')
@admin_required
def book_detail(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"success": False, "message": "图书不存在"}), 404

    borrow_records = book.borrow_records.order_by(BorrowRecord.borrow_date.desc()).all()
    return jsonify({
        "success": True,
        "data": {
            "book": book_to_dict(book),
            "borrow_records": [borrow_serializer(r) for r in borrow_records],
        }
    })


def borrow_serializer(r):
    return {
        'id': r.id, 'user_id': r.user_id, 'book_id': r.book_id,
        'user': r.user.username, 'book': r.book.title,
        'borrow_date': r.borrow_date.isoformat(),
        'due_date': r.due_date.isoformat(),
        'return_date': r.return_date.isoformat() if r.return_date else None,
        'status': r.status, 'fine': float(r.fine),
        'is_overdue': r.is_overdue,
    }


@admin_bp.route('/books/<int:book_id>', methods=['PUT'])
@admin_required
def book_edit(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"success": False, "message": "图书不存在"}), 404

    title = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    if not title or not author:
        return jsonify({"success": False, "message": "书名和作者不能为空"}), 400

    isbn = request.form.get('isbn', '').strip() or None
    if isbn and isbn != book.isbn:
        existing = Book.query.filter_by(isbn=isbn).first()
        if existing:
            return jsonify({"success": False, "message": "该ISBN已存在"}), 400

    book.title = title
    book.author = author
    book.isbn = isbn
    book.publisher = request.form.get('publisher', '').strip() or None
    publish_date = request.form.get('publish_date')
    book.publish_date = datetime.strptime(publish_date, '%Y-%m-%d').date() if publish_date else None
    category_id = request.form.get('category_id', type=int)
    book.category_id = category_id if category_id and category_id > 0 else None
    try:
        book.total_copies = int(request.form.get('total_copies', book.total_copies))
        book.available_copies = int(request.form.get('available_copies', book.available_copies))
    except ValueError:
        pass
    book.description = request.form.get('description', '').strip() or None
    book.location = request.form.get('location', '').strip() or None

    cover = request.files.get('cover_image')
    if cover and cover.filename:
        book.cover_image = save_upload_file(cover)

    db.session.commit()
    return jsonify({"success": True, "message": "图书更新成功", "data": book_to_dict(book)})


@admin_bp.route('/books/<int:book_id>', methods=['DELETE'])
@admin_required
def book_delete(book_id):
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"success": False, "message": "图书不存在"}), 404

    active_borrows = BorrowRecord.query.filter_by(book_id=book_id).filter(
        BorrowRecord.status.in_(['borrowed', 'overdue'])
    ).count()
    if active_borrows > 0:
        return jsonify({"success": False, "message": "该图书还有未归还的借阅记录，无法删除"}), 400

    db.session.delete(book)
    db.session.commit()
    return jsonify({"success": True, "message": "图书删除成功"})


# --- Category CRUD ---
def category_to_dict(c):
    return {
        'id': c.id, 'name': c.name, 'description': c.description,
        'book_count': c.books.count(),
    }


@admin_bp.route('/categories')
@admin_required
def category_list():
    categories = Category.query.order_by(Category.name).all()
    return jsonify({
        "success": True,
        "data": [category_to_dict(c) for c in categories]
    })


@admin_bp.route('/categories', methods=['POST'])
@admin_required
def category_add():
    name = request.get_json().get('name', '').strip()
    description = request.get_json().get('description', '').strip()
    if not name:
        return jsonify({"success": False, "message": "分类名称不能为空"}), 400
    if Category.query.filter_by(name=name).first():
        return jsonify({"success": False, "message": "该分类名称已存在"}), 400

    category = Category(name=name, description=description or None)
    db.session.add(category)
    db.session.commit()
    return jsonify({"success": True, "message": "分类添加成功", "data": category_to_dict(category)})


@admin_bp.route('/categories/<int:category_id>', methods=['PUT'])
@admin_required
def category_edit(category_id):
    category = db.session.get(Category, category_id)
    if not category:
        return jsonify({"success": False, "message": "分类不存在"}), 404

    name = request.get_json().get('name', '').strip()
    if name:
        existing = Category.query.filter_by(name=name).first()
        if existing and existing.id != category_id:
            return jsonify({"success": False, "message": "该分类名称已存在"}), 400
        category.name = name
    category.description = request.get_json().get('description', '').strip() or None
    db.session.commit()
    return jsonify({"success": True, "message": "分类更新成功", "data": category_to_dict(category)})


@admin_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@admin_required
def category_delete(category_id):
    category = db.session.get(Category, category_id)
    if not category:
        return jsonify({"success": False, "message": "分类不存在"}), 404
    if category.books.count() > 0:
        return jsonify({"success": False, "message": "该分类下还有图书，无法删除"}), 400

    db.session.delete(category)
    db.session.commit()
    return jsonify({"success": True, "message": "分类删除成功"})


# --- User CRUD ---
@admin_bp.route('/users')
@admin_required
def user_list():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)

    query = User.query
    if search:
        query = query.filter(
            db.or_(User.username.contains(search), User.email.contains(search))
        )

    query = query.order_by(User.created_at.desc())
    return jsonify(paginated_response(query, page, 10, lambda u: u.to_dict()))


@admin_bp.route('/users', methods=['POST'])
@admin_required
def user_add():
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not username or not email or not password:
        return jsonify({"success": False, "message": "请填写所有必填字段"}), 400
    if len(password) < 6:
        return jsonify({"success": False, "message": "密码长度不能少于6位"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"success": False, "message": "该用户名已存在"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "该邮箱已存在"}), 400

    user = User(
        username=username, email=email,
        role=data.get('role', 'user'), phone=data.get('phone', '').strip() or None,
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"success": True, "message": "用户添加成功", "data": user.to_dict()})


@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@admin_required
def user_edit(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"success": False, "message": "用户不存在"}), 404

    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()

    if username:
        existing = User.query.filter_by(username=username).first()
        if existing and existing.id != user_id:
            return jsonify({"success": False, "message": "该用户名已存在"}), 400
        user.username = username
    if email:
        existing = User.query.filter_by(email=email).first()
        if existing and existing.id != user_id:
            return jsonify({"success": False, "message": "该邮箱已存在"}), 400
        user.email = email

    user.role = data.get('role', user.role)
    user.phone = data.get('phone', '').strip() or None
    if data.get('password'):
        user.set_password(data['password'])
    db.session.commit()
    return jsonify({"success": True, "message": "用户更新成功", "data": user.to_dict()})


@admin_bp.route('/users/<int:user_id>/toggle', methods=['PUT'])
@admin_required
def user_toggle(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"success": False, "message": "用户不存在"}), 404

    current = get_current_user()
    if user.id == current.id:
        return jsonify({"success": False, "message": "不能禁用自己的账号"}), 400

    user.is_active = not user.is_active
    db.session.commit()
    status_text = '启用' if user.is_active else '禁用'
    return jsonify({"success": True, "message": f"用户已{status_text}", "data": user.to_dict()})


# --- Borrow Management ---
@admin_bp.route('/borrows')
@admin_required
def borrow_list():
    update_overdue_status()
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '', type=str)

    query = BorrowRecord.query
    if status_filter:
        query = query.filter_by(status=status_filter)

    query = query.order_by(BorrowRecord.created_at.desc())
    return jsonify(paginated_response(query, page, 10, borrow_serializer))


@admin_bp.route('/borrows', methods=['POST'])
@admin_required
def borrow_add():
    data = request.get_json()
    user_id = data.get('user_id')
    book_id = data.get('book_id')

    if not user_id or not book_id:
        return jsonify({"success": False, "message": "请选择用户和图书"}), 400

    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"success": False, "message": "图书不存在"}), 404
    if book.available_copies <= 0:
        return jsonify({"success": False, "message": "该图书库存不足，无法借阅"}), 400

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"success": False, "message": "用户不存在"}), 404

    record = BorrowRecord(
        user_id=user_id, book_id=book_id,
        borrow_date=datetime.utcnow(), due_date=get_due_date(),
        status=BorrowRecord.STATUS_BORROWED
    )
    book.available_copies -= 1
    db.session.add(record)
    db.session.commit()
    return jsonify({"success": True, "message": "借阅成功", "data": borrow_serializer(record)})


@admin_bp.route('/borrows/<int:record_id>/return', methods=['POST'])
@admin_required
def borrow_return(record_id):
    record = db.session.get(BorrowRecord, record_id)
    if not record:
        return jsonify({"success": False, "message": "借阅记录不存在"}), 404
    if record.status == BorrowRecord.STATUS_RETURNED:
        return jsonify({"success": False, "message": "该记录已归还"}), 400

    record.return_date = datetime.utcnow()
    record.status = BorrowRecord.STATUS_RETURNED
    record.fine = record.calculate_fine()
    record.book.available_copies += 1

    pending_reservation = Reservation.query.filter_by(
        book_id=record.book_id, status=Reservation.STATUS_PENDING
    ).order_by(Reservation.reserve_date.asc()).first()

    db.session.commit()

    msg = f"还书成功！逾期 {record.overdue_days} 天，罚金 ¥{record.fine:.2f}" if record.fine > 0 else "还书成功"
    return jsonify({"success": True, "message": msg, "data": borrow_serializer(record)})


# --- Reservation Management ---
def reservation_serializer(r):
    return {
        'id': r.id, 'user_id': r.user_id, 'book_id': r.book_id,
        'user': r.user.username, 'book': r.book.title,
        'reserve_date': r.reserve_date.isoformat(), 'status': r.status,
    }


@admin_bp.route('/reservations')
@admin_required
def reservation_list():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '', type=str)

    query = Reservation.query
    if status_filter:
        query = query.filter_by(status=status_filter)

    query = query.order_by(Reservation.created_at.desc())
    return jsonify(paginated_response(query, page, 10, reservation_serializer))


@admin_bp.route('/reservations/<int:reservation_id>/cancel', methods=['POST'])
@admin_required
def reservation_cancel(reservation_id):
    reservation = db.session.get(Reservation, reservation_id)
    if not reservation:
        return jsonify({"success": False, "message": "预约记录不存在"}), 404

    reservation.status = Reservation.STATUS_CANCELLED
    db.session.commit()
    return jsonify({"success": True, "message": "预约已取消"})


# --- Review Management ---
def review_serializer(r):
    return {
        'id': r.id, 'user_id': r.user_id, 'book_id': r.book_id,
        'user': r.user.username, 'book': r.book.title,
        'rating': r.rating, 'content': r.content,
        'is_visible': r.is_visible,
        'created_at': r.created_at.isoformat() if r.created_at else None,
    }


@admin_bp.route('/reviews')
@admin_required
def review_list():
    page = request.args.get('page', 1, type=int)
    query = Review.query.order_by(Review.created_at.desc())
    return jsonify(paginated_response(query, page, 10, review_serializer))


@admin_bp.route('/reviews/<int:review_id>/toggle', methods=['PUT'])
@admin_required
def review_toggle(review_id):
    review = db.session.get(Review, review_id)
    if not review:
        return jsonify({"success": False, "message": "评论不存在"}), 404

    review.is_visible = not review.is_visible
    db.session.commit()
    status_text = '显示' if review.is_visible else '隐藏'
    return jsonify({"success": True, "message": f"评论已{status_text}"})


@admin_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
@admin_required
def review_delete(review_id):
    review = db.session.get(Review, review_id)
    if not review:
        return jsonify({"success": False, "message": "评论不存在"}), 404

    db.session.delete(review)
    db.session.commit()
    return jsonify({"success": True, "message": "评论已删除"})


# --- Announcement Management ---
def announcement_serializer(a):
    return {
        'id': a.id, 'title': a.title, 'content': a.content,
        'priority': a.priority, 'is_published': a.is_published,
        'publisher': a.publisher.username if a.publisher else None,
        'created_at': a.created_at.isoformat() if a.created_at else None,
    }


@admin_bp.route('/announcements')
@admin_required
def announcement_list():
    page = request.args.get('page', 1, type=int)
    query = Announcement.query.order_by(Announcement.created_at.desc())
    return jsonify(paginated_response(query, page, 10, announcement_serializer))


@admin_bp.route('/announcements', methods=['POST'])
@admin_required
def announcement_add():
    data = request.get_json()
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    if not title or not content:
        return jsonify({"success": False, "message": "标题和内容不能为空"}), 400

    current = get_current_user()
    announcement = Announcement(
        title=title, content=content,
        priority=data.get('priority', 'normal'),
        publisher_id=current.id
    )
    db.session.add(announcement)
    db.session.commit()
    return jsonify({"success": True, "message": "公告发布成功", "data": announcement_serializer(announcement)})


@admin_bp.route('/announcements/<int:announcement_id>', methods=['PUT'])
@admin_required
def announcement_edit(announcement_id):
    announcement = db.session.get(Announcement, announcement_id)
    if not announcement:
        return jsonify({"success": False, "message": "公告不存在"}), 404

    data = request.get_json()
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    if not title or not content:
        return jsonify({"success": False, "message": "标题和内容不能为空"}), 400

    announcement.title = title
    announcement.content = content
    announcement.priority = data.get('priority', announcement.priority)
    db.session.commit()
    return jsonify({"success": True, "message": "公告更新成功", "data": announcement_serializer(announcement)})


@admin_bp.route('/announcements/<int:announcement_id>/toggle', methods=['PUT'])
@admin_required
def announcement_toggle(announcement_id):
    announcement = db.session.get(Announcement, announcement_id)
    if not announcement:
        return jsonify({"success": False, "message": "公告不存在"}), 404

    announcement.is_published = not announcement.is_published
    db.session.commit()
    status_text = '发布' if announcement.is_published else '下架'
    return jsonify({"success": True, "message": f"公告已{status_text}"})


@admin_bp.route('/announcements/<int:announcement_id>', methods=['DELETE'])
@admin_required
def announcement_delete(announcement_id):
    announcement = db.session.get(Announcement, announcement_id)
    if not announcement:
        return jsonify({"success": False, "message": "公告不存在"}), 404

    db.session.delete(announcement)
    db.session.commit()
    return jsonify({"success": True, "message": "公告已删除"})
