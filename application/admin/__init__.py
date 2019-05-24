from flask import Blueprint, render_template
from flask_login import login_required
from datetime import datetime

bp = Blueprint('admin', __name__)

from application.admin import users, orders, orders_map, catalog, administrator


@bp.context_processor
def view_context_processor():
    return {
        'year': datetime.now().year
    }


@bp.route('/', methods=['GET', 'HEAD'])
@login_required
def index():
    return render_template('admin/index.html')
