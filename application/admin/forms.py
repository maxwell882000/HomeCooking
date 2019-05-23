from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField, SelectField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileAllowed
from application.core.models import Dish, DishCategory


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
