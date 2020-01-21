from flask import render_template, url_for, flash, redirect, request
from rent_app import app, db, bcrypt
from rent_app.forms import RegistrationForm, LoginForm, ChangePassword, RentForm
from rent_app.models import Car, User, Order, Basket
from flask_login import login_user, current_user, logout_user, login_required
import datetime

@app.route('/')
def home():
    return redirect(url_for('filter',cat= 'wszystkie'))

def stat_counter(car,to_count='opinions'):
    all_orders = Order.query.all()
    if to_count=='opinions':
        counts = [1 if order.car_id==car.id else 0 for order in all_orders].count(1)
    else:
        counts = len([val for val in [order.opinion if order.car_id == car.id else None for order in all_orders] if val])
    return counts

def print_date(dtime):
    return dtime.strftime("%d-%m-%Y %H:%M:%S")

def check_dates(val,start,end):
    if start == None or end == None:
        return True
    elif val.date() > end or val.date() < start:
        return True
    else:
        return False

def available(car_id, now=False, start_date=0, end_date=0):
    if now:
        orders = Order.query.filter_by(car_id = car_id)
        now_time = datetime.datetime.utcnow()
        avals = [check_dates(now_time, order.start_date, order.end_date) for order in orders]
        return 'TAK' if all(avals) else 'NIE'
    else:
        return False

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
@app.route('/car_profile', methods=["POST", "GET"])
def car_profile(car_id=0):
    car = Car.query.filter_by(id=int(car_id)).first()
    orders = Order.query.filter_by(car_id = car_id)
    users_id = [order.user_id for order in orders]
    users = [User.query.filter_by(id=u_id).first() for u_id in users_id]
    orders_users = zip(orders,users)
    car_aval = available(car.id, now=True)
    return render_template('car-profile.html', car=car, car_aval = car_aval, orders_users=orders_users )

@app.route('/filter/<cat>/')
@app.route('/filter/<cat>/<sort>')
def filter(cat, sort='alfa'):
    if cat == 'wszystkie':
        cars = Car.query.all()
    else:
        cars = Car.query.filter_by(category=cat)

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
@app.route('/basket/<option>/<int:car_id>', methods=['POST', 'GET'])
@login_required
def basket(option='show', car_id=0):
    if option=='add':
        in_basket = Basket.query.filter_by(user_id = current_user.id, car_id = car_id).first()
        if in_basket:
            flash('Wybrany samochód jest już w koszyku', 'danger')
        else:
            new_item = Basket(user_id = current_user.id, car_id = car_id)
            db.session.add(new_item)
            db.session.commit()
            flash('Dodano do koszyka!', 'success')
        return redirect(url_for('home'))
    elif option=='remove':
        to_remove = Basket.query.filter_by(user_id = current_user.id, car_id = car_id).one()
        db.session.delete(to_remove)
        db.session.commit()
        flash('Usunięto pozycję z koszyka!', 'info')
        return redirect(url_for('basket'))
    else:
        form = RentForm()
        basket_items = Basket.query.filter_by(user_id  = current_user.id)
        basket_cars_id = [item.car_id for item in basket_items]
        basket_cars = [Car.query.filter_by(id = car_id).first() for car_id in basket_cars_id]
        #basket_cars = db.engine.execute("SELECT * FROM car WHERE id IN (SELECT car_id FROM basket WHERE user_id= :val)", {'val':current_user.id})
        cars_ops = zip(basket_cars, [stat_counter(car) for car in basket_cars])
    return render_template('basket.html', cars_ops = cars_ops, form=form)


@app.route('/rent/<int:car_id>', methods=['POST','GET'])
@login_required
def rent(car_id):
    if not available(car_id, now=True):
        flash("Wybrany samochód jest obecnie niedostępny")
        return redirect(url_for('car_profile', car_id = car_id))
    car = Car.query.filter_by(id=car_id).first()
    form = RentForm()
    if form.validate_on_submit():
        car_id = form.car_id.data
        order = Order(car_id = car_id, user_id = current_user.id,
                      start_date = form.start_date.data, end_date=form.end_date.data ,
                      pay_option=form.payment.data)
        db.session.add(order)
        db.session.commit()
        flash("operacja przebiegła pomyślnie, hurra!",'success')
        return redirect(url_for('pay', order_id=order.order_id))
    return render_template('rent.html', payment=False, car=car, form=form)


@app.route('/pay/<int:order_id>', methods=['POST','GET'])
@app.route('/pay/<int:order_id>/<stat>', methods=['POST','GET'])
def pay(order_id, stat=""):
    if stat=="":
        order = Order.query.filter_by(order_id=order_id).first()
        car = Car.query.filter_by(id = order.car_id).first()
        to_pay = (order.end_date - order.start_date).days * car.price
        return render_template('rent.html', payment=True, order=order, to_pay=to_pay, car=car)
    else:
        order = Order.query.filter_by(order_id=order_id).first()
        order.status = "Zapłacone"
        db.session.commit()
        flash("Wpłata została odnotowana!")
        return redirect(url_for('account', option="history"))


