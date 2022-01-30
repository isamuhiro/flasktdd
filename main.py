from http import HTTPStatus
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import MultiDict
from flask_marshmallow import Marshmallow

from product.product_form import ProductForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@app.route('/')
def hello():
    return 'Hello World!'


@app.get('/product')
def get_products():
    products = Product.query.all()
    return jsonify(products_schema.dump(products)), HTTPStatus.OK


@app.post('/product')
def create_product():
    form = ProductForm(MultiDict(request.json))

    if not form.validate():
        return jsonify(form.errors), HTTPStatus.BAD_REQUEST

    product = Product(name=form.name.data, price=form.price.data)
    db.session.add(product)
    db.session.commit()

    response = product_schema.dump(product)

    app.logger.info(f"/product [{response}]]")
    return response, HTTPStatus.CREATED


@app.route('/product/<int:id>')
def get_product(id):
    product = Product.query.filter_by(id=id).first()
    if not product:
        app.logger.warning(f'Product {id} was not found. {HTTPStatus.NOT_FOUND}')
        return jsonify(message='Product %s was not found'), HTTPStatus.NOT_FOUND

    response = product_schema.dump(product)
    app.logger.info(f"/product [{response}]]")
    return jsonify(response), HTTPStatus.OK


if __name__ == '__main__':
    app.run()
