from flask import * #импортирует все
from database.operations import select, call_proc
from access import group_required
from database.sql_provider import SQLProvider
import os

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


# Словарь с отчетами
report_list = [
    {'rep_name':'Отчёт 1 ', 'rep_id':'1'},
    {'rep_name':'Отчёт 2 ', 'rep_id':'2'}
]

# Словарь с URL-ами для создания и просмотра отчетов
report_url = {
    '1': {'create_rep':'bp_report.create_rep1', 'view_rep':'bp_report.view_rep1'},
    '2': {'create_rep':'bp_report.create_rep2', 'view_rep':'bp_report.view_rep2'}
}


@blueprint_report.route('/', methods=['GET', 'POST'])
def start_report():
    if request.method == 'GET':
        return render_template('menu_report.html', report_list=report_list)
    else:
        rep_id = request.form.get('rep_id') # Если метод POST, получаем идентификатор отчета из формы
        if request.form.get('create_rep'): # Проверяем, какая кнопка была нажата: создать отчет или просмотреть отчет
            url_rep = report_url[rep_id]['create_rep']
        else:
            url_rep = report_url[rep_id]['view_rep']
        return redirect(url_for(url_rep)) # Перенаправляем пользователя на соответствующий URL


@blueprint_report.route('/create_rep1', methods=['GET', 'POST'])
@group_required
def create_rep1():
    if request.method == 'GET':
        return render_template('report_create.html')
    else:
        rep_month = request.form.get('input_month')
        rep_year = request.form.get('input_year')
        if rep_year and rep_month:
            _sql = provider.get('rep1.sql', in_year=rep_year, in_month=rep_month)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if product_result:
                return "Такой отчёт уже существует"
            else:
                res = call_proc(current_app.config['db_config'], 'product_report_new', rep_month, rep_year)
                print('res=', res)
                return render_template('report_created.html')
        else:
            return "Repeat input"


@blueprint_report.route('/view_rep1', methods=['GET', 'POST'])
@group_required
def view_rep1():
    if request.method == 'GET':
        return render_template('view_rep.html')
    else:
        rep_month = request.form.get('input_month')
        rep_year = request.form.get('input_year')
        if rep_year and rep_month:
            _sql = provider.get('rep1.sql', in_year=rep_year, in_month=rep_month)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if product_result:
                return render_template('result_rep1.html', schema=["№", "Месяц", "Год", "Продукт №", "Кол-во"], result=product_result)
            else:
                return "Такой отчёт не был создан"
        else:
            return "Repeat input"

# заглушки
@blueprint_report.route('/create_rep2')
@group_required
def create_rep2():
    print("GET_create2")
    return "Вы создаете Отчёт 2"

@blueprint_report.route('/view_rep2')
@group_required
def view_rep2():
    print("GET_create2")
    return "Вы просматриваете Отчёт 2"
