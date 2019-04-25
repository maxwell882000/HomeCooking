from application import db
from application.core.models import Dish, DishCategory


def get_all_categories() -> DishCategory:
    return DishCategory.query.all()


def get_dishes_by_category_name(name: str) -> list:
    dish_category = DishCategory.query.filter(DishCategory.name == name).get()
    if dish_category:
        return dish_category.dishes.all()
    return []


def get_dish_by_name(name: str) -> Dish:
    dish = Dish.query.filter(Dish.name == name).get()
    return dish
