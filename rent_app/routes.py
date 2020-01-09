from flask import render_template, url_for, flash, redirect, request
from rent_app import app, db, bcrypt
from rent_app.forms import RegistrationForm, LoginForm, ChangePassword, RentForm
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


@app.route('/car_profile/<int:car_id>', methods=["POST", "GET"])
def car_profile(car_id):
    form = RentForm()
    if form.validate_on_submit():
        order = Order(car_id = car_id, user_id = current_user.id, start_date = form.start_date.data, end_date=form.end_date.data)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('account'))
    else:
        car = Car.query.filter_by(id=int(car_id)).first()
        return render_template('car-profile.html', car=car, form=form)

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

@app.route('/account/<option>', methods=["POST", "GET"])
@login_required
def account(option):
    form = ChangePassword()
    if option=="change_passwd":
        if form.validate_on_submit():
            current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.session.commit()
            flash('hasło zostało zmienione!', 'success')
            return redirect(url_for('account', option='history'))
        else:
            return render_template('change_passwd.html', form=form)
    else:
        orders = Order.query.filter_by(user_id=current_user.id)
        cars_id = [order.car_id for order in orders]
        cars = [Car.query.filter_by(id=car_id).first() for car_id in cars_id]
        orders_cars = zip(orders,cars)
        return render_template('account.html',orders_cars=orders_cars )