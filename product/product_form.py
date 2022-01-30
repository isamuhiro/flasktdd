from wtforms import Form, StringField, FloatField, validators


class ProductForm(Form):
    name = StringField('name', [validators.InputRequired()])
    price = FloatField('price', [validators.InputRequired()])
