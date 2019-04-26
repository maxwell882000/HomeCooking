from application import db
from application.core.models import User, UserAdmin
from . import dishservice


def is_user_exists(user_id: int):
    return User.query.get(user_id) is not None


def register_user(user_id: int, username: str):
    user = User(id=user_id, username=username)
    db.session.add(user)
    db.session.commit()


def set_user_name(user_id: int, user_name: str):
    user = User.query.get(user_id)
    user.name = user_name
    db.session.commit()


def set_user_phone_number(user_id: int, phone_number: str):
    user = User.query.get(user_id)
    user.phone_number = phone_number
    db.session.commit()


def set_user_language(user_id: int, language: str):
    user = User.query.get(user_id)
    user.language = language
    db.session.commit()


def set_user_company(user_id: int, company_name: str):
    user = User.query.get(user_id)
    user.company_name = company_name
    db.session.commit()


def get_user_by_id(user_id: int):
    return User.query.get(user_id)


def get_admin_user_by_email(email: str) -> UserAdmin:
    return UserAdmin.query.filter(UserAdmin.email == email).first()


def get_admin_user_by_id(id: int) -> UserAdmin:
    return UserAdmin.query.get(id)


def is_user_registered(user_id):
    user = User.query.get(user_id)
    if user is None:
        return False
    return user.name is not None and user.phone_number is not None


def get_user_language(user_id: int):
    user = User.query.get(user_id)
    return user.language


def set_user_admin_password(user: UserAdmin, password: str):
    user.set_password(password)
    db.session.commit()


def is_admin_user_exists(email):
    return get_admin_user_by_email(email) is not None


def get_all_bot_users():
    return User.query.all()


def get_user_cart(user_id: int) -> list:
    user = get_user_by_id(user_id)
    return user.cart.all()


def clear_user_cart(user_id: int):
    user = get_user_by_id(user_id)
    dishes = [cart_item.dish for cart_item in user.cart.all()]
    for dish in dishes:
        user.remove_dish_from_cart(dish)
    db.session.commit()


def remove_dish_from_user_cart(user_id: int, dish_name: str, language: str) -> bool:
    user = get_user_by_id(user_id)
    dish = dishservice.get_dish_by_name(dish_name, language)
    if not dish:
        return False
    user.remove_dish_from_cart(dish)
    db.session.commit()
    return True
