from application.admin import bp
from flask_login import login_required
from flask import render_template, redirect, url_for, flash
from application.core import dishservice
from application.admin.forms import CategoryForm, DishForm


@login_required
@bp.route('/catalog', methods=['GET'])
def catalog():
    categories = dishservice.get_all_categories()
    return render_template('admin/catalog.html', title='Каталог', area='catalog', categories=categories)


@login_required
@bp.route('/catalog/<int:category_id>', methods=['GET', 'POST'])
def category(category_id: int):
    form = CategoryForm()
    if form.validate_on_submit():
        name_ru = form.name_ru.data
        name_uz = form.name_uz.data
        dishservice.update_category(category_id, name_ru, name_uz)
        flash('Категория {} | {} изменена'.format(name_ru, name_uz))
        return redirect(url_for('admin.catalog'))
    category = dishservice.get_category_by_id(category_id)
    form.fill_from_object(category)
    return render_template('admin/category.html',
                           title='{} | {}'.format(category.name, category.name_uz),
                           area='catalog', form=form, category=category)


@login_required
@bp.route('/catalog/create', methods=['GET', 'POST'])
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name_ru = form.name_ru.data
        name_uz = form.name_uz.data
        dishservice.create_category(name_ru, name_uz)
        flash('Категория {} | {} добавлена'.format(name_ru, name_uz))
        return redirect(url_for('admin.catalog'))
    return render_template('admin/new_category.html', title='Добавить категорию', area='catalog', form=form)


@login_required
@bp.route('/catalog/<int:category_id>/remove', methods=['GET'])
def remove_category(category_id: int):
    dishservice.remove_category(category_id)
    return redirect(url_for('admin.catalog'))


@login_required
@bp.route('/catalog/dish/create', methods=['GET', 'POST'])
def create_dish():
    form = DishForm()
    all_categories = dishservice.get_all_categories()
    form.category.choices = [(c.id, '{} | {}'.format(c.name, c.name_uz)) for c in all_categories]
    if form.validate_on_submit():
        name_ru = form.name_ru.data
        name_uz = form.name_uz.data
        description_ru = form.description_ru.data
        description_uz = form.description_uz.data
        image = form.image.data
        price = form.price.data
        category_id = form.category.data
        new_dish = dishservice.create_dish(name_ru, name_uz, description_ru, description_uz, image, price, category_id)
        flash('Блюдо {} | {} успешно добавлено в категорию {} | {}'.format(
            name_ru, name_uz, new_dish.category.name, new_dish.category.name_uz
        ), category='success')
        return redirect(url_for('admin.catalog'))
    return render_template('admin/new_dish.html', title="Добавить блюдо", area='catalog', form=form)


@login_required
@bp.route('/catalog/dish/<int:dish_id>', methods=['GET', 'POST'])
def dish(dish_id: int):
    form = DishForm()
    all_categories = dishservice.get_all_categories()
    form.category.choices = [(c.id, '{} | {}'.format(c.name, c.name_uz)) for c in all_categories]
    if form.validate_on_submit():
        name_ru = form.name_ru.data
        name_uz = form.name_uz.data
        description_ru = form.description_ru.data
        description_uz = form.description_uz.data
        image = form.image.data
        price = form.price.data
        category_id = form.category.data
        delete_image = form.delete_image.data
        dishservice.update_dish(dish_id, name_ru, name_uz, description_ru, description_uz,
                                image, price, category_id, delete_image)
        flash('Блюдо {} | {} изменено'.format(name_ru, name_uz), category='success')
        return redirect(url_for('admin.catalog'))
    dish = dishservice.get_dish_by_id(dish_id)
    form.fill_from_object(dish)
    return render_template('admin/dish.html', title='{} | {}'.format(dish.name, dish.name_uz),
                           area='catalog', form=form, dish=dish)


@login_required
@bp.route('/catalog/dish/<int:dish_id>/remove', methods=['GET'])
def remove_dish(dish_id: int):
    dishservice.remove_dish(dish_id)
    return redirect(url_for('admin.catalog'))
