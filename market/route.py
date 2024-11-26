from flask import Blueprint, render_template, request, session, current_app, url_for
from werkzeug.utils import redirect
from database.sql_provider import SQLProvider
from database.connection import UseDatabase
import datetime
import os
from access import external_required
from database.operations import select_dict
from flasgger import swag_from

blueprint_market = Blueprint('bp_market', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@blueprint_market.route('/', methods=['GET', 'POST'])
@external_required
@swag_from({
    'responses': {
        200: {
            'description': 'Displays the product list or updates the basket',
            'content': {
                'text/html': {}
            }
        }
    },
    'parameters': [
        {
            'name': 'prod_id',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': 'ID of the product to add to the basket (POST request only)'
        }
    ]
})
def order_index():
    db_config = current_app.config['db_config']
    if request.method == 'GET':
        sql = provider.get('product_list.sql')
        items = select_dict(db_config, sql)
        basket_items = session.get('basket', {})
        return render_template('product_list.html', items=items, basket=basket_items)
    else:
        prod_id = request.form['prod_id']
        sql = provider.get('product_list.sql')
        items = select_dict(db_config, sql)
        add_to_basket(prod_id, items)
        return redirect(url_for('bp_market.order_index'))

@blueprint_market.route('/save_order', methods=['GET', 'POST'])
@swag_from({
    'responses': {
        200: {
            'description': 'Saves the current basket as an order and clears it',
            'content': {
                'text/html': {}
            }
        }
    }
})
def save_order():
    user_id = session.get('user_id')
    current_basket = session.get('basket', {})
    order_id = save_order_with_list(current_app.config['db_config'], user_id, current_basket)
    if order_id:
        session.pop('basket')
        return render_template('order_created.html', order_id=order_id)
    else:
        return 'Что-то пошло не так'

@blueprint_market.route('/clear-basket')
@swag_from({
    'responses': {
        302: {
            'description': 'Clears the current basket and redirects to the product list',
            'headers': {
                'Location': {
                    'description': 'Redirect URL',
                    'type': 'string'
                }
            }
        }
    }
})
def clear_basket():
    if 'basket' in session:
        session.pop('basket')
    return redirect(url_for('bp_market.order_index'))
