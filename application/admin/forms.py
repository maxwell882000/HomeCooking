from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField, SelectField, BooleanField, \
    PasswordField, FloatField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from flask_wtf.file import FileAllowed
from application.core.models import Dish, DishCategory
import settings
from flask_login import current_user


class CategoryForm(FlaskForm):
    name_ru = StringField('Название на русском', validators=[DataRequired('Укажите название категории на русском')])
    name_uz = StringField('Название на узбекском', validators=[DataRequired('Укажите название категории на узбексокм')])
    submit = SubmitField('Сохранить')

    def fill_from_object(self, category: DishCategory):
        self.name_ru.data = category.name
        self.name_uz.data = category.name_uz


class DishForm(FlaskForm):
    name_ru = StringField('Название на русском', validators=[DataRequired('Укажите название блюда на русском')])
    name_uz = StringField('Название на узбекском', validators=[DataRequired('Укажите название блюда на узбексокм')])
    description_ru = TextAreaField('Описание блюда на русском',
                                   validators=[DataRequired('Укажите описание блюда на русском')])
    description_uz = TextAreaField('Описание блюда на узбекском',
                                   validators=[DataRequired('Укажите описание блюда на узбекском')])
    category = SelectField('Категория', validators=[DataRequired('Укажите категорию')], coerce=int)
    price = StringField('Цена', validators=[DataRequired('Укажите цену')])
    image = FileField('Изображение',
                      validators=[FileAllowed(['png', 'jpg'],
                                              message='Разрешены только изображения форматов .jpg, .png')])
    delete_image = BooleanField('Удалить изображение')
    submit = SubmitField('Сохранить')

    def fill_from_object(self, dish: Dish):
        self.name_ru.data = dish.name
        self.name_uz.data = dish.name_uz
        self.description_uz.data = dish.description_uz
        self.description_ru.data = dish.description
        self.category.default = dish.category_id
        self.price.data = dish.price

    def validate_price(self, field):
        if not field.data.isdigit():
            raise ValidationError('Укажите числовое значение цены')
        if int(field.data) <= 0:
            raise ValidationError('Цена не может быть отрицательной или равной нулю')


class AdministratorEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Укажите e-mail')])
    password = PasswordField('Пароль', validators=[DataRequired('Для смены e-mail необходима аутентификация')])
    submit = SubmitField('Изменить')

    def fill_from_current_user(self):
        self.email.data = current_user.email

    def validate_password(self, field):
        if not current_user.check_password(field.data):
            raise ValidationError('Указан неверный пароль')


class AdministratorPasswordForm(FlaskForm):
    current_password = PasswordField('Текущий пароль',
                                     validators=[DataRequired('Для смены пароля укажите текущий пароль')])
    new_password = PasswordField('Новый пароль', validators=[DataRequired("Введите новый пароль")])
    password_confirmation = PasswordField('Подтвердите новый пароль',
                                          validators=[EqualTo('new_password', 'Пароли должны совпадать')])
    submit = SubmitField('Изменить')


    def validate_password(self, field):
        if not current_user.check_password(field.data):
            raise ValidationError('Указан неверный пароль')


class DeliveryPriceForm(FlaskForm):
    first_3_km = StringField('Стоимость за первые три киллометра',
                             validators=[DataRequired('Укажите стоимость первых трёх километров')])
    others_km = StringField('Стоимость за остальной путь',
                            validators=[DataRequired('Укажите стоимость за остальные километры')])
    submit = SubmitField('Сохранить')

    def fill_from_settings(self):
        delivery_cost = settings.get_delivery_cost()
        self.first_3_km.data = delivery_cost[0]
        self.others_km.data = delivery_cost[1]


class CafeLocationForm(FlaskForm):
    latitude = FloatField('Широта', validators=[DataRequired("Укажите широту")])
    longitude = FloatField('Долгота', validators=[DataRequired('Укажите долготу')])
    submit = SubmitField('Сохранить')

    def fill_from_settings(self):
        coordinates = settings.get_cafe_coordinates()
        self.latitude.data = coordinates[0]
        self.longitude.data = coordinates[1]
