import os
from flask import Blueprint, render_template, request, current_app
from database.operations import select_dict
from database.sql_provider import SQLProvider
from access import group_required


blueprint_query = Blueprint('bp_query', __name__, template_folder='template')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@blueprint_query.route('/query')
def query_menu():
    return render_template('query.html')

@blueprint_query.route('/first_query', methods=['GET', 'POST'])
@group_required
def query_index1():
    if request.method == 'POST':
        prod_category = request.form.get('prod_category')
        prod_price = request.form.get('prod_price')
        _sql = provider.get('product.sql', prod_category=prod_category, prod_price=prod_price)
        products = select_dict(current_app.config['db_config'], _sql)
        if products:
            prod_title = 'Вот результат из БД'
            return render_template('dynamic.html', prod_title=prod_title, products=products)
        else:
            return 'Ошибка'
    return render_template('input_param.html')

@blueprint_query.route('/second_query', methods=['GET', 'POST'])
@group_required
def query_index2():
    if request.method == 'POST':
        prod_category = request.form.get('prod_category')
        _sql = provider.get('product2.sql', prod_category=prod_category)
        products = select_dict(current_app.config['db_config'], _sql)
        if products:
            prod_title = 'Вот результат из БД'
            return render_template('dynamic2.html', prod_title=prod_title, products=products)
        else:
            return 'Ошибка'
    return render_template('input_param2.html')