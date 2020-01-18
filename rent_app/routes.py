from flask import render_template, url_for, flash, redirect, request
from rent_app import app, db, bcrypt
from rent_app.forms import RegistrationForm, LoginForm, ChangePassword, RentForm
from rent_app.models import Car, User, Order
from flask_login import login_user, current_user, logout_user, login_required
import datetime

@app.route('/')
def home():
    return redirect(url_for('filter',cat= 'wszystkie'))

def print_date(dtime):
    return dtime.strftime("%d-%m-%Y %H:%M:%S")


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
    if request.method=="POST":
        order = Order(car_id = car_id, user_id = current_user.id, start_date = request.args.get('start_date'), end_date=request.args.get('end_date'))
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('account', option='history'))
    else:
        car = Car.query.filter_by(id=int(car_id)).first()
        orders = Order.query.filter_by(car_id = car_id)
        users_id = [order.user_id for order in orders]
        users = [User.query.filter_by(id=u_id).first() for u_id in users_id]
        orders_users = zip(orders,users)
        return render_template('car-profile.html', car=car, orders_users=orders_users )

@app.route('/filter/<cat>/')
@app.route('/filter/<cat>/<sort>')
def filter(cat, sort='alfa'):
    if cat == 'wszystkie':
        cars = Car.query.all()
    else:
        cars = Car.query.filter_by(category=cat)

    def stat_counter(car,to_count='opinions'):
        all_orders = Order.query.all()
        if to_count=='opinions':
            counts = [1 if order.car_id==car.id else 0 for order in all_orders].count(1)
        else:

            counts = len([val for val in [order.opinion if order.car_id == car.id else None for order in all_orders] if val])
        return counts

    if sort=='opinie':
        cars = [(car, stat_counter(car,'opinions')) for car in cars]
        cars = sorted(cars, key=lambda car: car[1], reverse = True)
        opinions = [car[1] for car in cars]
        cars = [car[0] for car in cars]
        cars_ops = zip(cars, opinions)
    elif sort=='popular':
        cars = [(car, stat_counter(car,'rents')) for car in cars]
        cars = sorted(cars, key=lambda car: car[1], reverse=True)
        cars = [car[0] for car in cars]
        cars_ops = zip(cars, [stat_counter(car) for car in cars])
    else:
        cars = sorted(cars, key=lambda car: car.brand + " " + car.model)
        cars_ops = zip(cars, [stat_counter(car) for car in cars])

    return render_template('home.html', cars_ops = cars_ops, category=cat)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account/<option>', methods=["POST", "GET"])
@login_required
def account(option):
    form = ChangePassword()
    if option == "change_passwd":
        if form.validate_on_submit():
            current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.session.commit()
            flash('hasło zostało zmienione!', 'success')
            return redirect(url_for('account', option='history'))
        else:
            return render_template('change_passwd.html', form=form)
    elif option=='add_opinion':
        order_id = int(request.form['order_id'])
        order = Order.query.filter_by(order_id= order_id ).first()
        order.opinion = request.form['opinion_text'].strip()
        order.opinion_date = datetime.datetime.utcnow()
        db.session.commit()
        flash('Opinia została zaktualizowana!', 'success')
        return redirect(url_for('account', option='history'))
    else:
        orders = Order.query.filter_by(user_id=current_user.id)
        cars_id = [order.car_id for order in orders]
        cars = [Car.query.filter_by(id=car_id).first() for car_id in cars_id]
        orders_cars = zip(orders,cars)
        return render_template('account.html',orders_cars=orders_cars)

@app.route('/basket', methods=['POST', 'GET'])
def basket():
    return render_template('basket.html')