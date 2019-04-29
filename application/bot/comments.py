from application import telegram_bot as bot
from application.core import commentservice, userservice
from application.resources import strings, keyboards
from telebot.types import Message


def check_auth(message: Message):
    return userservice.is_user_registered(message.from_user.id)


def check_comments(message: Message):
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)
    return strings.get_string('main_menu.send_comment', language) in message.text and 'private' in message.chat.type


@bot.message_handler(commands=['/comment'])
@bot.message_handler(content_types='text', func=lambda m: check_auth(m) and check_comments(m))
def comments(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    comments_message = strings.get_string('comments.send_comment', language)
    comments_keyboard = keyboards.get_keyboard('comments.send_comment', language)
    bot.send_message(chat_id, comments_message, reply_markup=comments_keyboard)
    bot.register_next_step_handler_by_chat_id(chat_id, comments_processor)


def comments_processor(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)

    def error():
        error_msg = strings.get_string('comments.error', language)
        bot.send_message(chat_id, error_msg)
        bot.register_next_step_handler_by_chat_id(chat_id, comments_processor)

    if not message.text:
        error()
        return
    if strings.get_string('go_to_menu', language) in message.text:
        main_menu_message = strings.get_string('main_menu.choose_option', language)
        main_menu_keyboard = keyboards.get_keyboard('main_menu', language)
        bot.send_message(chat_id, main_menu_message, reply_markup=main_menu_keyboard)
    else:
        commentservice.add_comment(user_id, message.text)
        thanks_message = strings.get_string('comments.thanks', language)
        main_menu_keyboard = keyboards.get_keyboard('main_menu', language)
        bot.send_message(chat_id, thanks_message, reply_markup=main_menu_keyboard)
