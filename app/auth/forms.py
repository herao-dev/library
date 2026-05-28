from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models.user import User


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired('请输入用户名')])
    password = PasswordField('密码', validators=[DataRequired('请输入密码')])
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired('请输入用户名'),
        Length(min=2, max=64, message='用户名长度需在2-64个字符之间')
    ])
    email = StringField('邮箱', validators=[
        DataRequired('请输入邮箱'),
        Email('请输入有效的邮箱地址')
    ])
    password = PasswordField('密码', validators=[
        DataRequired('请输入密码'),
        Length(min=6, max=128, message='密码长度至少6位')
    ])
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired('请确认密码'),
        EqualTo('password', message='两次输入的密码不一致')
    ])
    submit = SubmitField('注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')