from application import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


cart_items = db.Table('cart_items',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('dish_id', db.Integer, db.ForeignKey('dish.id'), primary_key=True),
                      db.Column('count', db.Integer))

order_items = db.Table('order_items',
                       db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
                       db.Column('dish_id', db.Integer, db.ForeignKey('dish.id'), primary_key=True),
                       db.Column('count', db.Integer))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    language = db.Column(db.String(5))
    cart = db.relationship('Dish', secondary=cart_items, lazy='dynamic')


class UserAdmin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True)
    password_hash = db.Column(db.String(120))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class DishCategory(db.Model):
    __tablename__ = 'dish_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    dishes = db.relationship('Dish', lazy='dynamic', backref='category')


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image_id = db.Column(db.String)
    description = db.Column(db.String(500))
    price = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('dish_categories.id'))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.Integer)
    order_items = db.relationship('Dish', secondary=order_items, lazy='dynamic',
                                  backref=db.backref('orders', lazy=True))

    class OrderTypes:
        PICK_UP = 1
        DELIVERY = 2


@login.user_loader
def load_user(id):
    return UserAdmin.query.get(int(id))
