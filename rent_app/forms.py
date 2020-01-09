from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from rent_app.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Hasło', validators = [DataRequired()])
    password2 = PasswordField('Powtórz Hasło', validators = [DataRequired(),EqualTo('password')])
    submit = SubmitField('Zarejestruj')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Podana nazwa użytkownika jest zajęta')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Podany email jest zajęty')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Hasło', validators = [DataRequired()])
    remember = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')


class ChangePassword(FlaskForm):
    password = PasswordField('Nowe Hasło', validators = [DataRequired()])
    password2 = PasswordField('Powtórz Hasło', validators = [DataRequired(),EqualTo('password')])
    submit = SubmitField('Aktualizuj')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Podana nazwa użytkownika jest zajęta')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Podany email jest zajęty')


class RentForm(FlaskForm):
    start_date = DateField('Data wypożyczenia: ', validators=[DataRequired()])
    end_date = DateField('Data zwrotu: ', validators=[DataRequired()])
    submit = SubmitField('Wypożycz')


