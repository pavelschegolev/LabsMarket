from functools import wraps

from flask import session, render_template, current_app, request, redirect, url_for


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs): # Определение внутренней функции wrapper, которая замещает оригинальную функцию. Принимает произвольное количество позиционных и ключевых аргументов.
        if 'user_id' in session: # Проверка наличия ключа 'user_id' в объекте сессии.
            return func(*args, **kwargs) # Если 'user_id' присутствует в сессии, вызывается оригинальная функция func с переданными аргументами.
        return redirect(url_for('blueprint_auth.start_auth'))
    return wrapper


def group_validation(config: dict) -> bool:
    endpoint_func = request.endpoint # имя блюпринта.имя обработчика
    endpoint_app = request.endpoint.split('.')[0] # имя блюпринта
    if 'user_group' in session:
        user_group = session['user_group']
        if user_group in config and endpoint_app in config[user_group]: # существует ли указанный блюпринт для данной группы пользователя в конфигурации.
            return True
        elif user_group in config and endpoint_func in config[user_group]: # существует ли указанный обработчик для данной группы пользователя в конфигурации.
            return True
    return False


def group_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config'] # Получение конфигурации доступа из текущего объекта приложения.
        if group_validation(config):
            return f(*args, **kwargs)
        return render_template('exceptions/internal_only.html')
    return wrapper


def external_validation(config):
    endpoint_func = request.endpoint # имя блюпринта.имя обработчика
    endpoint_app = request.endpoint.split('.')[0] # имя блюпринта
    user_id = session.get('user_id', None)
    user_group = session.get('user_group', None)
    if user_id and user_group is None: # Проверка, что пользователь внешний (не принадлежит к какой-либо группе).
        if endpoint_app in config['external']: # Проверка, существует ли указанный блюпринт для внешних пользователей в конфигурации.
            return True
        elif endpoint_func in config['external']: # Проверка, существует ли указанный обработчик для внешних пользователей в конфигурации.
            return True
    return False

def external_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config']
        if external_validation(config):
            return f(*args, **kwargs)
        return render_template('exceptions/external_only.html')
    return wrapper
