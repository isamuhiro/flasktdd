from http import HTTPStatus
from flask import Flask, jsonify, request

from product.ProductForm import ProductForm

app = Flask(__name__)

products = [dict(id=1, name='chicken breast', price=20.9),
            dict(id=2, name='rice 1kg', price=5.9)]


@app.route('/')
def hello():
    return 'Hello World!'


@app.get('/product')
def get_products():
    app.logger.info("'/product [%s]'", products)
    return jsonify(products), HTTPStatus.OK


@app.post('/product')
def create_product():
    form = ProductForm(request.form)
    if not form.validate():
        return jsonify(form.errors), HTTPStatus.BAD_REQUEST

    id_generator = max([product['id'] for product in products]) + 1
    product_response = dict(id=id_generator, name=form.name.data, price=form.price.data)
    products.append(product_response)

    app.logger.info("'/product [%s]'", products)
    return jsonify(product_response), HTTPStatus.CREATED


@app.route('/product/<int:id>')
def get_product(id):
    if id not in [product['id'] for product in products]:
        app.logger.warn("'/product [%s]'", products)
        return 'Product %s was not found', HTTPStatus.NOT_FOUND

    app.logger.info("'/product [%s]'", products)
    product = next(product for product in products if id == product['id'])
    return jsonify(product), HTTPStatus.OK


if __name__ == '__main__':
    app.run()
