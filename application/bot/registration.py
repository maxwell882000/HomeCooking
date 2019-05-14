from application import telegram_bot
from application.core import userservice
from application.resources import strings, keyboards
from telebot.types import Message


def process_user_language(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    def error():
        error_msg = strings.get_string('welcome.say_me_language')
        telegram_bot.send_message(chat_id, error_msg)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, process_user_language)

    if not message.text:
        error()
        return
    if message.text.startswith('/'):
        error()
        return
    if strings.get_string('language.russian') in message.text:
        language = 'ru'
    elif strings.get_string('language.uzbek') in message.text:
        language = 'uz'
    else:
        error()
        return
    userservice.register_user(user_id, message.from_user.username, language)
    success_message = strings.get_string('welcome.registration_successfully', language)
    main_menu_keyboard = keyboards.get_keyboard('main_menu', language)
    telegram_bot.send_message(chat_id, success_message, reply_markup=main_menu_keyboard)


@telegram_bot.message_handler(commands=['start'], func=lambda m: m.chat.type == 'private')
def welcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if userservice.is_user_registered(user_id):
        language = userservice.get_user_language(user_id)
        main_menu_message = strings.get_string('main_menu.choose_option', language)
        main_menu_keyboard = keyboards.get_keyboard('main_menu', language)
        telegram_bot.send_message(chat_id, main_menu_message, reply_markup=main_menu_keyboard)
        return
    welcome_text = strings.get_string('welcome')
    language_keyboard = keyboards.get_keyboard('welcome.language')
    msg = telegram_bot.send_message(chat_id, welcome_text, parse_mode='HTML', reply_markup=language_keyboard)
    telegram_bot.register_next_step_handler(msg, process_user_language)
