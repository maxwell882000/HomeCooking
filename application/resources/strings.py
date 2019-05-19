import os
import json
from application.core.models import Dish, Order

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
    cart_contains += '<b>{}</b>:'.format(get_string('catalog.cart', language))
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
    dish_str_template = '{name}\n\n{description}\n\n{price_str}: {price} {sum_str}'
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


def from_order_shipping_method(value: str, language: str) -> str:
    return get_string('order.' + value, language)


def from_order_payment_method(value: str, language: str) -> str:
    return get_string('order.' + value, language)


def from_order(order: Order, language: str, total: int) -> str:
    order_content = "<b>{}:</b>".format(get_string('your_order', language))
    order_content += '\n\n'
    order_content += '<b>{phone}:</b> {phone_value}\n'.format(phone=get_string('phone', language),
                                                              phone_value=order.phone_number)
    order_content += '<b>{payment_type}:</b> {payment_type_value}\n' \
        .format(payment_type=get_string('payment', language),
                payment_type_value=from_order_payment_method(order.payment_method, language))
    order_content += '<b>{shipping_method}:</b> {shipping_method_value}\n'.format(
        shipping_method=get_string('shipping_method', language),
        shipping_method_value=from_order_shipping_method(order.shipping_method, language)
    )
    if order.address_txt:
        order_content += '<b>{address}:</b> {address_value}'.format(address=get_string('address', language),
                                                                    address_value=order.address_txt)
    elif order.location:
        order_content += '<b>{address}:</b> {address_value}'.format(address=get_string('address', language),
                                                                    address_value=order.location.address)
    order_content += '\n\n'
    order_item_tmpl = '<b>{name}</b>\n{count} x {price} = {sum} {sum_str}\n'
    for order_item in order.order_items.all():
        dish = order_item.dish
        if language == 'uz':
            dish_name = dish.name_uz
        else:
            dish_name = dish.name
        order_item_str = order_item_tmpl.format(name=dish_name,
                                                count=order_item.count,
                                                price=_format_number(dish.price),
                                                sum=_format_number(order_item.count * dish.price),
                                                sum_str=get_string('sum', language))
        order_content += order_item_str
    order_content += "<b>{}</b>: {} {}".format(get_string('cart.summary', language),
                                               _format_number(total),
                                               get_string('sum', language))
    if order.delivery_price:
        order_content += '\n\n'
        order_content += '<i>{}</i>: {} {}'.format(get_string('delivery_price', language),
                                                   order.delivery_price,
                                                   get_string('sum', language))
        order_content += '\n\n'
        order_content += '<i>{}</i>'.format(get_string('order.delivery_price_helper', language))
    return order_content


def from_order_notification(order: Order, total_sum):
    order_content = "<b>Новый заказ!</b>"
    order_content += '\n\n'
    order_content += '<b>Номер телефона:</b> {}\n'.format(order.phone_number)
    order_content += '<b>Способ доставки:</b> {}\n'.format(from_order_shipping_method(order.shipping_method, 'ru'))
    order_content += '<b>Способ оплаты:</b> {}\n'.format(from_order_payment_method(order.payment_method, 'ru'))
    if order.address_txt:
        order_content += '<b>Адрес:</b> {}'.format(order.address_txt)
    elif order.location:
        order_content += '<b>Адрес:</b> {}'.format(order.location.address)
    order_content += '\n\n'
    order_item_tmpl = '<b>{name}</b>\n{count} x {price} = {sum} сум\n'
    for order_item in order.order_items.all():
        dish = order_item.dish
        dish_name = dish.name
        order_item_str = order_item_tmpl.format(name=dish_name,
                                                count=order_item.count,
                                                price=_format_number(dish.price),
                                                sum=_format_number(order_item.count * dish.price))
        order_content += order_item_str
    order_content += "<b>Общая стоимость заказа</b>: {} сум".format(_format_number(total_sum))
    if order.delivery_price:
        order_content += '\n\n'
        order_content += '<b>Стоимость доставки</b>: {} сум'.format(_format_number(order.delivery_price))
    return order_content
