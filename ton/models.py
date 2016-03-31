from flask_security import RoleMixin, UserMixin

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Authorization tables
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email


# Data tables
locations_services = db.Table(
    'locations_services',
    db.Column('location_id', db.Integer, db.ForeignKey('location.id')),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id'))
)


locations_zipcodes = db.Table(
    'locations_zipcodes',
    db.Column('location_id', db.Integer, db.ForeignKey('location.id')),
    db.Column('zipcode_id', db.Integer, db.ForeignKey('zip_code.id'))
)


locations_days_of_week = db.Table(
    'locations_days_of_week',
    db.Column('location_id', db.Integer, db.ForeignKey('location.id')),
    db.Column('day_of_week_id', db.Integer, db.ForeignKey('day_of_week.id'))
)


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    def __str__(self):
        return self.name


class Currency(db.Model):
    __tablename__ = 'currency'
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(80), unique=True)

    def __str__(self):
        return self.currency


class DayOfWeek(db.Model):
    __tablename__ = 'day_of_week'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), nullable=False, unique=True)

    def __str__(self):
        return self.day


class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(255))
    address_line1 = db.Column(db.String(80))
    address_line2 = db.Column(db.String(80))
    address_line3 = db.Column(db.String(80))
    phone = db.Column(db.String(30))
    contact_email = db.Column(db.String(256))
    website = db.Column(db.String(256))
    opening_time = db.Column(db.Time)
    closing_time = db.Column(db.Time)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    currency = db.relationship('Currency', backref='locations')
    min_cost = db.Column(db.Integer)
    days_of_week = db.relationship(
        'DayOfWeek', secondary=locations_days_of_week,
        backref=db.backref('locations', lazy='dynamic'))
    services = db.relationship(
        'Service', secondary=locations_services,
        backref=db.backref('locations', lazy='dynamic'))
    zip_codes = db.relationship(
        'Zipcode', secondary=locations_zipcodes,
        backref=db.backref('locations', lazy='dynamic'))

    def __str__(self):
        return self.name


class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)

    def __str__(self):
        return self.name


class Zipcode(db.Model):
    __tablename__ = 'zip_code'
    id = db.Column(db.Integer, primary_key=True)
    zip = db.Column(db.String(5), nullable=False, unique=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    city = db.relationship("City", backref="zip_codes")

    def __str__(self):
        return self.zip
