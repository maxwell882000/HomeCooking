from application import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class CartItem(db.Model):
    __tablename__ = 'cart_items'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), primary_key=True)
    count = db.Column(db.Integer)
    dish = db.relationship('Dish')


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), primary_key=True)
    count = db.Column(db.Integer)
    dish = db.relationship('Dish')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    language = db.Column(db.String(5))
    cart = db.relationship('CartItem', lazy='dynamic', backref='user')
    orders = db.relationship('Order', lazy='dynamic', backref='customer')

    def _dish_in_cart(self, dish) -> bool:
        """
        Check if dish is exists in cart
        :param dish: Dish
        :return: Check's result
        """
        return self.cart.filter(CartItem.dish_id == dish.id).count() > 0

    def add_dish_to_cart(self, dish, count):
        """
        Add a dish to cart if there isn't it in cart.
        And add cart item to database session
        :param dish: Dish
        :param count: Numbers of the dish
        :return: void
        """
        if self._dish_in_cart(dish):
            return
        cart_item = CartItem(count=count, dish=dish)
        self.cart.append(cart_item)
        db.session.add(cart_item)

    def remove_dish_from_cart(self, dish):
        """
        Remove dish from cart if it exists
        :param dish: Dish
        :return: void
        """
        cart_item = self.cart.filter(CartItem.dish_id == dish.id).get()
        if not cart_item:
            return
        self.cart.remove(cart_item)


class UserAdmin(db.Model, UserMixin):
    __tablename__ = 'user_admins'
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
    __tablename__ = 'dishes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image_id = db.Column(db.String)
    description = db.Column(db.String(500))
    price = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('dish_categories.id'))


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.Integer)
    order_items = db.relationship('OrderItem', lazy='dynamic',
                                  backref='order')

    class OrderTypes:
        PICK_UP = 1
        DELIVERY = 2


@login.user_loader
def load_user(id):
    return UserAdmin.query.get(int(id))
