from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from application.core import userservice


class LoginEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Email обязателен'), Email('Неверный формат e-mail')])
    submit = SubmitField('Продолжить')

    def validate_email(self, email: StringField):
        if not userservice.is_admin_user_exists(email.data):
            raise ValidationError('Такой email не зарегистрирован')


class LoginPasswordForm(FlaskForm):
    password = PasswordField('Введите свой пароль', validators=[DataRequired('Необходимо ввести пароль')])
    submit = SubmitField('Вход')


class CreateNewPasswordForm(FlaskForm):
    password = PasswordField('Введите новый пароль', validators=[DataRequired(message='Пароль обязателен')])
    password_confirmation = PasswordField('Повторите пароль',
                                          validators=[DataRequired('Пароль необходимо повторить'),
                                                      EqualTo('password', 'Пароли должны совпадать')])
    submit = SubmitField('Сохранить')
