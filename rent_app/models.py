from datetime import date
from rent_app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password= db.Column(db.String(60), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True )

    def __repr__(self):
        return f'User("{self.username}", "{self.email}")'

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(30), nullable=False)
    image_file = db.Column(db.String(30), nullable=False)
    brand = db.Column(db.String(30), nullable=False)
    model = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    prod_year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    gearcase = db.Column(db.String(10))
    fuel = db.Column(db.String(10))


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable = False, default = date.today())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    start_date = db.Column(db.Date, default = date.today())
    end_date = db.Column(db.Date, default = date.today())
    opinion = db.Column(db.String(250))
    opinion_date = db.Column(db.DateTime)
    pay_option = db.Column(db.String(30))
    status=db.Column(db.String(30), default="W trakcie")

class Basket(db.Model):
    item_id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    pay_option = db.Column(db.String(30))
    status=db.Column(db.String(30), default="W trakcie")
