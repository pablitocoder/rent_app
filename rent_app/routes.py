from flask import render_template, url_for, flash, redirect, request
from rent_app import app, db, bcrypt
from rent_app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from rent_app.models import Car, User, Order
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def home():
    cars = Car.query.all()
    return render_template('home.html', cars = cars)

@app.route('/about')
def about():
    return '<h2>About Page</h2>'

@app.route('/register', methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'I cyk,  {form.username.data} zarejestrowany/a!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Nieudane Logowanie, spróbuj ponownie', 'danger')
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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account', methods=["POST", "GET"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('you account has been updated','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', form=form)