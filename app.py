import json
from flask import Flask, render_template, session
from query.route import blueprint_query
from report.route import blueprint_report
from access import login_required
from auth.routes import blueprint_auth
from market.route import blueprint_market

from flasgger import Swagger, swag_from
import os

app = Flask(__name__, template_folder='template')  # Создание объекта Flask

# Инициализация Swagger с расширенной конфигурацией
swagger = Swagger(app, template_file='swagger_config.yml')

# Регистрация Blueprint'ов с указанием URL-префиксов
app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_market, url_prefix='/market')

# Загрузка конфигураций базы данных и настроек доступа из JSON-файлов
with open('datafiles/db_config.json', 'r') as f:
    app.config['db_config'] = json.load(f)
with open('datafiles/access_config.json', 'r') as f:
    app.config['access_config'] = json.load(f)

app.secret_key = 'BBQ s@use'

# Маршрут для отображения главного меню после успешного входа в систему
@app.route('/')
@swag_from({
    'responses': {
        200: {
            'description': 'Returns the main menu based on user group',
            'content': {
                'text/html': {}
            }
        }
    }
})
def menu_choice():
    if session.get('user_group', None):
        return render_template('internal_user_menu.html')
    return render_template('external_user_menu.html')

@app.route('/exit')
@login_required
@swag_from({
    'responses': {
        200: {
            'description': 'Clears the session and returns the exit page',
            'content': {
                'text/html': {}
            }
        }
    }
})
def exit_func():
    session.clear()
    return render_template('exit.html')

# Функция для сохранения Swagger-документации в JSON файл
# Функция для сохранения Swagger-документации в JSON файл
def save_swagger_spec():
    with app.app_context():  # Создать контекст приложения
        swagger_spec = swagger.get_apispecs()
        output_file = os.path.join(os.path.dirname(__file__), 'swagger_spec.json')
        with open(output_file, 'w') as f:
            json.dump(swagger_spec, f, indent=2)
        print(f"Swagger specification saved to {output_file}")

# Запуск приложения при выполнении файла
if __name__ == '__main__':
    save_swagger_spec()  # Сохранить Swagger-документацию
    app.run(host='127.0.0.1', port=5001, debug=True)

