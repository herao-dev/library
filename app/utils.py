import os
import uuid
from datetime import datetime, timedelta
from flask import current_app
from werkzeug.utils import secure_filename


def save_upload_file(file, subfolder='covers'):
    if not file or file.filename == '':
        return None

    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    unique_name = f"{uuid.uuid4().hex}.{ext}"

    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(upload_path, exist_ok=True)

    file_path = os.path.join(upload_path, unique_name)
    file.save(file_path)

    return f"uploads/{subfolder}/{unique_name}"


def get_due_date(borrow_days=None):
    if borrow_days is None:
        borrow_days = current_app.config.get('BORROW_DAYS', 30)
    return datetime.utcnow() + timedelta(days=borrow_days)


def update_overdue_status():
    from app.extensions import db
    from app.models.borrow import BorrowRecord

    overdue_records = BorrowRecord.query.filter(
        BorrowRecord.status == BorrowRecord.STATUS_BORROWED,
        BorrowRecord.due_date < datetime.utcnow()
    ).all()

    for record in overdue_records:
        record.status = BorrowRecord.STATUS_OVERDUE

    db.session.commit()
    return len(overdue_records)