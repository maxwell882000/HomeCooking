from application import telegram_bot
from application.core import userservice
from application.resources import strings, keyboards
from telebot.types import Message


def check_language(message: Message):

    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)
    return strings.get_string('main_menu.language', language) in message.text and message.chat.type == 'private'


def check_auth(message: Message):
    return userservice.is_user_registered(message.from_user.id)


def checker(message: Message):
    if not message.text:
        return False
    return check_auth(message) and check_language(message)


def _to_main_menu(chat_id, language, message_text=None):
    if message_text:
        main_menu_message = message_text
    else:
        main_menu_message = strings.get_string('main_menu.choose_option', language)
    main_menu_keyboard = keyboards.get_keyboard('main_menu', language)
    telegram_bot.send_message(chat_id, main_menu_message, reply_markup=main_menu_keyboard)


@telegram_bot.message_handler(commands=['language'])
@telegram_bot.message_handler(content_types=['text'], func=checker)
def language_handler(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    change_language_message = strings.get_string('language.change', language)
    change_language_keyboard = keyboards.from_change_language(language)
    telegram_bot.send_message(chat_id, change_language_message, reply_markup=change_language_keyboard)
    telegram_bot.register_next_step_handler_by_chat_id(chat_id, change_language_processor)


def change_language_processor(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        error_msg = strings.get_string('language.change', language)
        telegram_bot.send_message(chat_id, error_msg)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, change_language_processor)

    if not message.text:
        error()
        return
    if strings.get_string('go_back', language) in message.text:
        _to_main_menu(chat_id, language)
        return
    elif strings.get_string('language.russian') in message.text:
        new_language = 'ru'
        userservice.set_user_language(user_id, new_language)
    elif strings.get_string('language.uzbek') in message.text:
        new_language = 'uz'
    else:
        error()
        return
    userservice.set_user_language(user_id, new_language)
    success_message = strings.get_string('language.success', new_language)
    _to_main_menu(chat_id, new_language, success_message)
