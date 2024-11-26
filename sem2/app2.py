import json
from flask import Flask,request, render_template
from work_with_db import select_dict

app = Flask(__name__)
with open('data_files/db_config.json') as f:
    app.config['db_config'] = json.load(f)

@app.route('/')
@app.route('/<param>')

def hello_param(param=None):
    if param is None:
        return 'Hello world!'
    else:
        return f'hello {param}'

@app.route('/product', methods=['GET','POST'])
def product_index():
    if request.method =='GET':
        return render_template('input_param.html')
    else:
        category = request.form.get('category')                           #.form - словарь, ключом словаря будеть название category
        price = request.form.get('price')
        _sql= f"""select prod name, prod_measure, prod_price from product 
                  where prod_category={category} and prod_price>{price}"""
        products= select_dict(app.config['db_config'],_sql)
        if products:
            prod_title='вот полученный результат'
            render_template('dynamic.html',products=products,prod_title=prod_title)
        else:
            return 'Результат не получен'


       # return f''' Вы ввели категорию {category} и цену {price}'''

if __name__== '__main__' :
    app.run(host='127.0.0.1' ,port=5001, debug=True)