from application import db
from application.core.models import Dish, DishCategory
from application.core import exceptions
from typing import List
from application.utils import files
import os
from config import Config
from werkzeug.utils import secure_filename


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


def create_dish(name_ru, name_uz, description_ru, description_uz, image, price, category_id):
    dish = Dish(name=name_ru, name_uz=name_uz,
                description=description_ru, description_uz=description_uz,
                price=price, category_id=category_id)
    if image and image.filename != '':
        file_path = os.path.join(Config.UPLOAD_DIRECTORY, secure_filename(image.filename))
        files.save_file(image, file_path, recreate=True)
        dish.image_path = file_path
    db.session.add(dish)
    db.session.commit()


def dish_exists(dish_name: str, category_id: int):
    category = get_category_by_id(category_id)
    return category.dishes.filter(Dish.name == dish_name or Dish.name_uz == dish_name).count() > 0


def update_dish(dish_id, name_ru, name_uz, description_ru, description_uz, image, price, category_id):
    dish = get_dish_by_id(dish_id)
    dish.name = name_ru
    dish.name_uz = name_uz
    dish.description = description_ru
    dish.description_uz = description_uz
    dish.price = price
    dish.category_id = category_id
    if image and image.filename != '':
        files.remove_file(dish.image_path)
        file_path = os.path.join(Config.UPLOAD_DIRECTORY, secure_filename(image.filename))
        files.save_file(image, file_path)
        dish.image_id = None
        dish.image_path = file_path
    db.session.commit()


def remove_dish(dish_id: int):
    db.session.delete(Dish.query.get_or_404(dish_id))


def get_dish_by_id(dish_id: int):
    return Dish.query.get_or_404(dish_id)


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
