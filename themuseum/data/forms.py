from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = StringField('Введите почту', validators=[DataRequired()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    confirm = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Ваша фамилия', validators=[DataRequired()])
    name = StringField('Ваше имя', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    """форма авторизации"""
    email = EmailField('Введите почту', validators=[DataRequired()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RecoveryForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    surname = StringField('Ваша фамилия', validators=[DataRequired()])
    email = StringField('Введите почту', validators=[DataRequired()])
    submit = SubmitField('Восстановить доступ')


class FinalRecoveryForm(FlaskForm):
    email = StringField('Введите почту', validators=[DataRequired()])
    password = PasswordField('Введите новый пароль', validators=[DataRequired()])
    confirm = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Изменить пароль')




class ImageForm(FlaskForm):
    file = FileField('Фото', validators=[DataRequired()])
    submit = SubmitField('Загрузить фото')