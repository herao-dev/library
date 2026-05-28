from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional, EqualTo, ValidationError
from flask_login import current_user
from app.models.user import User


class ProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired('请输入用户名'), Length(min=2, max=64)])
    email = StringField('邮箱', validators=[DataRequired('请输入邮箱'), Email('请输入有效的邮箱地址')])
    phone = StringField('手机号', validators=[Optional(), Length(max=20)])
    submit = SubmitField('保存')

    def validate_username(self, field):
        existing = User.query.filter_by(username=field.data).first()
        if existing and existing.id != current_user.id:
            raise ValidationError('该用户名已被使用')

    def validate_email(self, field):
        existing = User.query.filter_by(email=field.data).first()
        if existing and existing.id != current_user.id:
            raise ValidationError('该邮箱已被使用')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('当前密码', validators=[DataRequired('请输入当前密码')])
    new_password = PasswordField('新密码', validators=[
        DataRequired('请输入新密码'),
        Length(min=6, max=128, message='密码长度至少6位')
    ])
    confirm_password = PasswordField('确认新密码', validators=[
        DataRequired('请确认新密码'),
        EqualTo('new_password', message='两次输入的密码不一致')
    ])
    submit = SubmitField('修改密码')