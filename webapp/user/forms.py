from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from webapp.user.models import User


class LoginForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
    )
    remember_me = BooleanField(
        'Запомнить меня', default=True,
        render_kw={'class': 'form-check-input'}
    )
    submit = SubmitField('Войти', render_kw={'class': 'btn btn-danger'})


class RegForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
    )
    password2 = PasswordField(
        'Подтвердите пароль',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={'class': 'form-control'}
    )
    submit = SubmitField('Войти', render_kw={'class': 'btn btn-danger'})

    def validate_username(self, username):
        users_counter = User.query.filter_by(username=username.data).count()
        if users_counter:
            raise ValidationError('Данный никнейм занят')

