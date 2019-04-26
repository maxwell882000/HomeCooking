import os
import json
from application.core.models import Dish

_basedir = os.path.abspath(os.path.dirname(__file__))

# Load strings from json
# Russian language
_strings_ru = json.loads(open(os.path.join(_basedir, 'strings_ru.json'), 'r', encoding='utf8').read())

# Uzbek language
_strings_uz = json.loads(open(os.path.join(_basedir, 'strings_uz.json'), 'r', encoding='utf8').read())


def _format_number(number: int):
    return '{0:,}'.format(number).replace(',', ' ')


def get_string(key, language='ru'):
    if language == 'ru':
        return _strings_ru.get(key, 'no_string')
    elif language == 'uz':
        return _strings_uz.get(key, 'no_string')
    else:
        raise Exception('Invalid language')


def from_cart_items(cart_items, language, total) -> str:
    cart_contains = ''
    cart_contains += '<b>{}</b>:' % get_string('catalog.cart', language)
    cart_contains += '\n\n'
    cart_str_item = "<b>{name}</b>\n{count} x {price} = {sum}"
    for cart_item in cart_items:
        if language == 'uz':
            dish_item = cart_str_item.format(name=cart_item.dish.name_uz,
                                             count=cart_item.count,
                                             price=_format_number(cart_item.dish.price),
                                             sum=_format_number(cart_item.count * cart_item.dish.price))
        else:
            dish_item = cart_str_item.format(name=cart_item.dish.name,
                                             count=cart_item.count,
                                             price=_format_number(cart_item.dish.price),
                                             sum=_format_number(cart_item.count * cart_item.dish.price))
        dish_item += " {}\n".format(get_string('sum', language))
        cart_contains += dish_item
    cart_contains += "\n<b>{}</b>: {} {}".format(get_string('cart.summary', language),
                                                 _format_number(total),
                                                 get_string('sum', language))

    return cart_contains


def from_dish(dish: Dish, language: str) -> str:
    dish_str_template = '{name}\n\n{description\n\n{price_str}: {price} {sum_str}}'
    if language == 'uz':
        dish_str = dish_str_template.format(name=dish.name_uz,
                                            description=dish.description_uz,
                                            price_str=get_string('dish.price', language),
                                            price=_format_number(dish.price),
                                            sum_str=get_string('sum', language))
    else:
        dish_str = dish_str_template.format(name=dish.name,
                                            description=dish.description,
                                            price_str=get_string('dish.price', language),
                                            price=_format_number(dish.price),
                                            sum_str=get_string('sum', language))
    return dish_str
