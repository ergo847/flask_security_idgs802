from wtforms import Form, StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired

class ProductForm(Form):
    nombre = StringField('Nombre', [DataRequired()], render_kw={"class": "input"})
    imagen = FileField('Imagen', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Solo se permiten imágenes en formato JPG, JPEG o PNG')], render_kw={"class": "input"})
    descripcion = TextAreaField('Descripción del producto', validators=[DataRequired(), Length(min=10, max=500)], render_kw={"class": "input"})
    precio = IntegerField('Precio del producto', validators=[DataRequired(), NumberRange(min=1)], render_kw={"class": "input"})
    stock = IntegerField('Stock del producto', validators=[DataRequired(), NumberRange(min=0)], render_kw={"class": "input"})
    image_url = StringField('Imagen del producto', validators=[DataRequired(), Length(min=1, max=500)], render_kw={"class": "file-input is-primary"})