from flask_security import RoleMixin, UserMixin

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class Service(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(40), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


services_locations = db.Table(
    'services_locations',
    db.Column('location_id', db.Integer(), db.ForeignKey('location.id')),
    db.Column('service_id', db.Integer(), db.ForeignKey('service.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    zip = db.Column(db.String(5))
    services = db.relationship('Service', secondary=services_locations,
                               backref=db.backref('locations', lazy='dynamic'))

    def __str__(self):
        return "{zip}: {name}".format(name=self.name, zip=self.zip)
