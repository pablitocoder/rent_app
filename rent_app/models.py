from datetime import datetime
from rent_app import db

class User(db.Model):
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
    order_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    opinion = db.Column(db.String(250))
    opinion_date = db.Column(db.DateTime)
    status=db.Column(db.String(30))
