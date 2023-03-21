#Importamos la clase UserMixin de  flask_login
from flask_security import UserMixin, RoleMixin
from . import db

user_roles = db.Table('user_roles',
  db.Column('userId', db.Integer, db.ForeignKey('user.id')),
  db.Column('roleId', db.Integer, db.ForeignKey('role.id')),
)

class User(UserMixin, db.Model):
    """User account model."""
    
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship('Role',
      secondary=user_roles,
      backref = db.backref('users', lazy='dynamic')
    )

class Role(RoleMixin, db.Model):
    """Role model"""

    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

class Product(db.Model):
    """Product model"""

    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
