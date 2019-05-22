from application import db
from application.core.models import Dish, DishCategory
from application.core import exceptions
from typing import List


def get_all_categories() -> List[DishCategory]:
    return DishCategory.query.all()


def get_category_by_id(category_id) -> DishCategory:
    return DishCategory.query.get_or_404(category_id)


def update_category(category_id: int, name_ru: str, name_uz:str):
    category = DishCategory.query.get_or_404(category_id)
    category.name = name_ru
    category.name_uz = name_uz
    db.session.commit()
    return category


def category_exists(category_name: str) -> bool:
    return DishCategory.query.filter(DishCategory.name == category_name or DishCategory.name_uz == category_name).count() > 0


def create_category(name_ru: str, name_uz: str):
    category = DishCategory(name=name_ru, name_uz=name_uz)
    db.session.add(category)
    db.session.commit()


def remove_category(category_id: int):
    db.session.delete(DishCategory.query.get_or_404(category_id))


def get_dishes_by_category_name(name: str, language: str) -> list:
    if language == 'uz':
        dish_category = DishCategory.query.filter(DishCategory.name_uz == name).first()
    else:
        dish_category = DishCategory.query.filter(DishCategory.name == name).first()
    if dish_category:
        return dish_category.dishes.all()
    else:
        raise exceptions.CategoryNotFoundError()


def get_dish_by_name(name: str, language: str) -> Dish:
    if language == 'uz':
        dish = Dish.query.filter(Dish.name_uz == name).first()
    else:
        dish = Dish.query.filter(Dish.name == name).first()
    return dish


def get_dish_by_id(dish_id: int):
    return Dish.query.get(dish_id)


def set_dish_image_id(dish: Dish, image_id: str):
    dish.image_id = image_id
    db.session.commit()
