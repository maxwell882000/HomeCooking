from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from application.resources.strings import get_string

_keyboards_ru = {
    'remove': ReplyKeyboardRemove()
}
_keyboards_uz = {
    'remove': ReplyKeyboardRemove()
}

_default_value = ReplyKeyboardMarkup(resize_keyboard=True)
_default_value.add('no_keyboard')

# Initialization russian keyboards
_welcome_language = ReplyKeyboardMarkup(resize_keyboard=True)
_welcome_language.add(get_string('language.russian'), get_string('language.uzbek'))
_keyboards_ru['welcome.language'] = _welcome_language
_welcome_phone_number_ru = ReplyKeyboardMarkup(resize_keyboard=True)
_welcome_phone_number_ru.add(KeyboardButton(get_string('my_number'), request_contact=True))
_keyboards_ru['welcome.phone_number'] = _welcome_phone_number_ru
_main_menu_ru = ReplyKeyboardMarkup(resize_keyboard=True)
_main_menu_ru.add(get_string('main_menu.make_order'))
_main_menu_ru.add(get_string('main_menu.send_comment'))
_main_menu_ru.add(get_string('main_menu.settings'))
_keyboards_ru['main_menu'] = _main_menu_ru
_settings_ru = ReplyKeyboardMarkup(resize_keyboard=True)
_settings_ru.add(get_string('settings.change_user_name'), get_string('settings.change_phone_number'))
_settings_ru.add(get_string('settings.change_language')),
_settings_ru.add(get_string('go_back'))
_keyboards_ru['settings'] = _settings_ru
_go_back_ru = ReplyKeyboardMarkup(resize_keyboard=True)
_go_back_ru.add(get_string('go_back'))
_keyboards_ru['go_back'] = _go_back_ru
_settings_change_phone_ru = ReplyKeyboardMarkup(resize_keyboard=True)
_settings_change_phone_ru.add(KeyboardButton(get_string('my_number'), request_contact=True))
_settings_change_phone_ru.add(get_string('go_back'))
_keyboards_ru['settings.change_phone'] = _settings_change_phone_ru
_settings_choose_language_ru = ReplyKeyboardMarkup(resize_keyboard=True)
_settings_choose_language_ru.add(get_string('language.russian'))
_settings_choose_language_ru.add(get_string('language.uzbek'))
_settings_choose_language_ru.add(get_string('go_back'))
_keyboards_ru['settings.choose_language'] = _settings_choose_language_ru

# Initialization uzbek keyboards
_welcome_phone_number_uz = ReplyKeyboardMarkup(resize_keyboard=True)
_welcome_phone_number_uz.add(KeyboardButton(get_string('my_number', 'uz'), request_contact=True))
_keyboards_uz['welcome.phone_number'] = _welcome_phone_number_uz
_main_menu_uz = ReplyKeyboardMarkup(resize_keyboard=True)
_main_menu_uz.add(get_string('main_menu.make_order', 'uz'))
_main_menu_uz.add(get_string('main_menu.send_comment', 'uz'))
_main_menu_uz.add(get_string('main_menu.settings', 'uz'))
_keyboards_uz['main_menu'] = _main_menu_uz
_settings_uz = ReplyKeyboardMarkup(resize_keyboard=True)
_settings_uz.add(get_string('settings.change_user_name', 'uz'), get_string('settings.change_phone_number', 'uz'))
_settings_uz.add(get_string('settings.change_language', 'uz')),
_settings_uz.add(get_string('go_back', 'uz'))
_keyboards_uz['settings'] = _settings_uz
_go_back_uz = ReplyKeyboardMarkup(resize_keyboard=True)
_go_back_uz.add(get_string('go_back', 'uz'))
_keyboards_uz['go_back'] = _go_back_uz
_settings_change_phone_uz = ReplyKeyboardMarkup(resize_keyboard=True)
_settings_change_phone_uz.add(KeyboardButton(get_string('my_number', 'uz'), request_contact=True))
_settings_change_phone_uz.add(get_string('go_back', 'uz'))
_keyboards_uz['settings.change_phone'] = _settings_change_phone_uz
_settings_choose_language_uz = ReplyKeyboardMarkup(resize_keyboard=True)
_settings_choose_language_uz.add(get_string('language.russian'))
_settings_choose_language_uz.add(get_string('language.uzbek'))
_settings_choose_language_uz.add(get_string('go_back', 'uz'))
_keyboards_uz['settings.choose_language'] = _settings_choose_language_uz


def get_keyboard(key, language='ru'):
    if language == 'ru':
        return _keyboards_ru.get(key, _default_value)
    elif language == 'uz':
        return _keyboards_uz.get(key, _default_value)
    else:
        raise Exception('Invalid language')


def from_dish_categories(dish_categories, language: str) -> ReplyKeyboardMarkup:
    categories_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    categories_keyboard.add(get_string('go_back', language))
    for category in dish_categories:
        if language == 'uz':
            categories_keyboard.add(category.name_uz)
        else:
            categories_keyboard.add(category.name)
    return categories_keyboard


def from_dishes(dishes, language: str) -> ReplyKeyboardMarkup:
    dishes_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    dishes_keyboard.add(get_string('go_back', language))
    for dish in dishes:
        if language == 'uz':
            dishes_keyboard.add(dish.name_uz)
        else:
            dishes_keyboard.add(dish.name)
    return dishes_keyboard
