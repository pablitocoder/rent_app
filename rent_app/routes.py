from flask import render_template, url_for, flash, redirect
from rent_app import app
from rent_app.forms import RegistrationForm, LoginForm
from rent_app import db
from rent_app.models import Car

@app.route('/')
def home():
    cars = Car.query.all()
    return render_template('home.html', cars = cars)

@app.route('/about')
def about():
    return '<h2>About Page</h2>'

@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Konto dla użytkownika {form.username.data} zostało stworzone!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == "pass":
            flash('Zalogowano', 'success')
            return redirect(url_for('home'))
        else:
            flash('Nieudane Logowanie', 'danger')
    return render_template('login.html',title = 'Login', form = form)


@app.route('/car_profile/<int:car_id>')
def car_profile(car_id):
    car = Car.query.filter_by(id=int(car_id)).first()
    return render_template('car-profile.html', car=car)

@app.route('/filter/<cat>')
def filter(cat):
    if cat != '':
        cars = Car.query.filter_by(category=cat)
    else:
        cars = Car.query.all()
    return render_template('home.html', cars = cars)