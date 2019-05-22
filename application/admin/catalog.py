from application.admin import bp
from flask_login import login_required
from flask import render_template, redirect, url_for
from application.core import dishservice


@login_required
@bp.route('/catalog', methods=['GET'])
def catalog():
	categories = dishservice.get_all_categories()
	return render_template('admin/catalog.html', title='Каталог', area='catalog', categories=categories)


@login_required
@bp.route('/catalog/<int:category_id>', methods=['GET', 'POST'])
def category(category_id: int):
	pass


@login_required
@bp.route('/catalog/<int:category_id>/remove', methods=['GET'])
def remove_category(category_id: int):
	pass


@login_required
@bp.route('/catalog/dish/<int:dish_id>', methods=['GET', 'POST'])
def dish(dish_id: int):
	pass


@login_required
@bp.route('/catalog/dish/<int:dish_id>/remove', methods=['GET'])
def remove_dish(dish_id: int):
	pass
