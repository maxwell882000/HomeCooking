from application import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    language = db.Column(db.String(5))
    company_name = db.Column(db.String)


class UserAdmin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True)
    password_hash = db.Column(db.String(120))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return UserAdmin.query.get(int(id))
