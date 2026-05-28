from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DateField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, Email, ValidationError
from app.models.user import User
from app.models.book import Book
from app.models.category import Category


class BookForm(FlaskForm):
    title = StringField('书名', validators=[DataRequired('请输入书名'), Length(max=256)])
    author = StringField('作者', validators=[DataRequired('请输入作者'), Length(max=128)])
    isbn = StringField('ISBN', validators=[Optional(), Length(max=20)])
    publisher = StringField('出版社', validators=[Optional(), Length(max=128)])
    publish_date = DateField('出版日期', validators=[Optional()])
    category_id = SelectField('分类', coerce=int, validators=[Optional()])
    total_copies = IntegerField('总库存', validators=[DataRequired('请输入总库存'), NumberRange(min=1, message='库存至少为1')])
    available_copies = IntegerField('可借数量', validators=[DataRequired('请输入可借数量'), NumberRange(min=0, message='可借数量不能小于0')])
    description = TextAreaField('图书简介', validators=[Optional()])
    location = StringField('馆藏位置', validators=[Optional(), Length(max=64)])
    submit = SubmitField('保存')

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
        self.category_id.choices.insert(0, (0, '-- 请选择分类 --'))

    def validate_isbn(self, field):
        if field.data:
            existing = Book.query.filter_by(isbn=field.data).first()
            if existing:
                if not hasattr(self, '_book_id') or existing.id != self._book_id:
                    raise ValidationError('该ISBN已存在')


class CategoryForm(FlaskForm):
    name = StringField('分类名称', validators=[DataRequired('请输入分类名称'), Length(max=64)])
    description = TextAreaField('分类描述', validators=[Optional()])
    submit = SubmitField('保存')


class UserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired('请输入用户名'), Length(min=2, max=64)])
    email = StringField('邮箱', validators=[DataRequired('请输入邮箱'), Email('请输入有效的邮箱地址')])
    password = PasswordField('密码', validators=[Optional(), Length(min=6, max=128, message='密码长度至少6位')])
    phone = StringField('手机号', validators=[Optional(), Length(max=20)])
    role = SelectField('角色', choices=[('user', '普通用户'), ('admin', '管理员')], validators=[DataRequired()])
    submit = SubmitField('保存')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self._user_id = None

    def set_user_id(self, user_id):
        self._user_id = user_id

    def validate_username(self, field):
        existing = User.query.filter_by(username=field.data).first()
        if existing and (self._user_id is None or existing.id != self._user_id):
            raise ValidationError('该用户名已被使用')

    def validate_email(self, field):
        existing = User.query.filter_by(email=field.data).first()
        if existing and (self._user_id is None or existing.id != self._user_id):
            raise ValidationError('该邮箱已被使用')


class BorrowForm(FlaskForm):
    user_id = SelectField('借阅用户', coerce=int, validators=[DataRequired('请选择用户')])
    book_id = SelectField('借阅图书', coerce=int, validators=[DataRequired('请选择图书')])
    submit = SubmitField('确认借阅')

    def __init__(self, *args, **kwargs):
        super(BorrowForm, self).__init__(*args, **kwargs)
        self.user_id.choices = [(u.id, f'{u.username} ({u.email})') for u in User.query.filter_by(is_active=True).order_by(User.username).all()]
        self.user_id.choices.insert(0, (0, '-- 请选择用户 --'))
        self.book_id.choices = [(b.id, f'{b.title} - {b.author} (可借:{b.available_copies})') for b in Book.query.filter(Book.available_copies > 0).order_by(Book.title).all()]
        self.book_id.choices.insert(0, (0, '-- 请选择图书 --'))


class AnnouncementForm(FlaskForm):
    title = StringField('公告标题', validators=[DataRequired('请输入公告标题'), Length(max=256)])
    content = TextAreaField('公告内容', validators=[DataRequired('请输入公告内容')])
    priority = SelectField('优先级', choices=[
        ('normal', '普通'),
        ('important', '重要'),
        ('urgent', '紧急')
    ], validators=[DataRequired()])
    submit = SubmitField('保存')