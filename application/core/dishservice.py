from application import db
from application.core.models import Dish, DishCategory


def get_all_categories() -> DishCategory:
    return DishCategory.query.all()


def get_dishes_by_category_name(name: str, language: str) -> list:
    if language == 'uz':
        dish_category = DishCategory.query.filter(DishCategory.name_uz == name).get()
    else:
        dish_category = DishCategory.query.filter(DishCategory.name == name).get()
    if dish_category:
        return dish_category.dishes.all()
    return []


def get_dish_by_name(name: str, language: str) -> Dish:
    if language == 'uz':
        dish = Dish.query.filter(Dish.name_uz == name).get()
    else:
        dish = Dish.query.filter(Dish.name == name).get()
    return dish
