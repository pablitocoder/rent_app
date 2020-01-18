from rent_app import db
from rent_app.models import User, Car, Order, Basket
"""
db.drop_all()
db.create_all()

ls = [
Car(category='osobowe', image_file='tesla-x.jpg',brand='Tesla', model='Model X', type='hatchback', price = 360, prod_year=2019, seats=7, fuel='elektryczny', gearcase='automtyczna'),
Car(category='osobowe', image_file='insignia.jpg',brand='Opel', model='Insignia A', type='sedan', price = 290, prod_year=2016, seats=5, fuel='diesel', gearcase='manualna'),
Car(category='sportowe', image_file='mustang.jpg',brand='Ford', model='Mustang', type='coupe', price = 245, prod_year=2017, seats=4, fuel='benzyna', gearcase='manualna'),
Car(category='osobowe', image_file='audi-a6.jpg',brand='Audi', model='A6', type='sedan', price = 190, prod_year=2015, seats=5, fuel='diesel', gearcase='automtyczna'),
Car(category='sportowe', image_file='bmw-m2.jpg',brand='BMW', model='M2', type='coupe', price = 240, prod_year=2016, seats=5, fuel = 'benzyna', gearcase='manualna'),
Car(category='sportowe', image_file='panamera.jpg',brand='Porsche', model='panamera', type='coupe', price = 350, prod_year=2015, seats=4, fuel='hybryda', gearcase='automtyczna'),
Car(category='terenowe', image_file='wrangler-3.jpg',brand='Jeep', model='Wrangler 3', type='SUV', price = 310, prod_year=2014, seats=5, fuel='benzyna', gearcase='manualna'),
Car(category='terenowe', image_file='hummer.jpg',brand='Hummer', model='H2', type='SUV', price = 410, prod_year=2008, seats=5, fuel='benzyna', gearcase='manualna'),
Car(category='osobowe', image_file='caravelle.jpg',brand='Volkswagen', model='Caravelle', type='minivan', price = 200, prod_year=2013, seats=9, fuel='diesel', gearcase='automtyczna'),
Car(category='dostawcze', image_file='transit.jpg',brand='Ford', model='Transit', type='furgon', price = 200, prod_year=2017, seats=3, fuel='benzyna', gearcase='manualna'),
Car(category='klasyki', image_file='syrena.jpg',brand='FSO', model='Syrena', type='sedan', price = 280, prod_year=1977, seats=5, fuel='benzyna', gearcase='manualna'),
Car(category='klasyki', image_file='warszawa.jpg',brand='FSO', model='Warszawa', type='sedan', price = 280, prod_year=1972, seats=5, fuel='benzyna', gearcase='manualna'),
Car(category='klasyki', image_file='wolga.jpg',brand='Wołga', model='GAZ 21', type='sedan', price = 240, prod_year=1961, seats=5, fuel='benzyna', gearcase='manualna'),
Car(category='klasyki', image_file='bentley.jpg',brand='Bentley', model=' ', type='sedan', price = 320, prod_year=1950, seats=5, fuel='benzyna', gearcase='manualna'),
Car(category='klasyki', image_file='golf.jpg',brand='Volkswagen', model='Golf 1', type='hatchback', price = 290, prod_year=1979, seats=5, fuel='benzyna', gearcase='manualna')
]

for car in ls:
    db.session.add(car)
db.session.commit()
"""