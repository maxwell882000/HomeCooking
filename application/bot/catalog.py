from application import telegram_bot as bot
from application.core import userservice, dishservice
from application.resources import strings, keyboards
from telebot.types import Message
from application.core import exceptions


def check_catalog(message: Message):
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)
    return strings.get_string('main_menu.make_order', language) in message.text and 'private' in message.chat.type


def check_auth(message: Message):
    return userservice.is_user_registered(message.from_user.id)


def back_to_the_catalog(chat_id, language, message_txt=None):
    bot.send_chat_action(chat_id, 'typing')
    if not message_txt:
        catalog_message = strings.get_string('catalog.start', language)
    else:
        catalog_message = message_txt
    categories = dishservice.get_all_categories()
    category_keyboard = keyboards.from_dish_categories(categories, language)
    bot.send_message(chat_id, catalog_message, reply_markup=category_keyboard)
    bot.register_next_step_handler_by_chat_id(chat_id, catalog_processor)


def choose_dish_processor(message: Message):
    pass


def catalog_processor(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        error_message = strings.get_string('catalog.error', language)
        bot.send_message(chat_id, error_message)
        bot.register_next_step_handler_by_chat_id(chat_id, catalog_processor)

    if not message.text:
        error()
        return
    if strings.get_string('go_back', language) in message.text:
        back_to_the_catalog(chat_id, language)
        return
    try:
        dishes = dishservice.get_dishes_by_category_name(message.text, language)
    except exceptions.CategoryNotFoundError:
        error()
        return
    dish_message = strings.get_string('catalog.choose_dish', language)
    dishes_keyboard = keyboards.from_dishes(dishes, language)
    bot.send_message(chat_id, dish_message, reply_markup=dishes_keyboard)
    bot.register_next_step_handler_by_chat_id(chat_id, choose_dish_processor)


@bot.message_handler(commands=['order'], func=check_auth)
@bot.message_handler(content_types=['text'], func=lambda m: check_auth(m) and check_catalog(m))
def catalog(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)
    bot.send_chat_action(chat_id, 'typing')
    catalog_message = strings.get_string('catalog.start', language)
    categories = dishservice.get_all_categories()
    category_keyboard = keyboards.from_dish_categories(categories, language)
    bot.send_message(chat_id, catalog_message, reply_markup=category_keyboard)
    bot.register_next_step_handler_by_chat_id(chat_id, catalog_processor)
