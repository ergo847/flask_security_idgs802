from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_security import login_required, current_user
from flask_security.decorators import roles_accepted, roles_required
from flask_login import login_required, current_user
from sqlalchemy import func
import os
from werkzeug.utils import secure_filename
import configparser
import uuid

config = configparser.ConfigParser()
config.read('config.cfg')



import project.forms as forms

from .models import User, Product
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    productos = Product.query.order_by(func.random()).limit(3).all()
    datos = {
        'user': current_user,
        'productos': productos
    }
    return render_template('index.html', datos = datos)

@main.route('/profile')
@login_required
def profile():
    datos = {
        'user': current_user,
    }
    return render_template('profile.html', datos = datos)

@main.route('/productos')
@login_required
def productos():
    productos = Product.query.all()
    datos = {
        'user': current_user,
        'productos': productos
    }
    return render_template('productos.html', datos = datos)

@main.route('/productos/<int:id>')
@login_required
# @roles_accepted('admin','user')
def producto_get(id):
    producto = Product.query.get_or_404(id)
    if producto:
        datos = {
            'user': current_user,
            'producto': producto
        }
        return render_template('producto.html', datos = datos)
    else:
        flash('El producto no existe')
        return redirect(url_for('main.productos'))


@main.route('/contacto')
@login_required
def contacto():
    datos = {
        'user': current_user,
    }
    return render_template('contacto.html', datos = datos)

# Rutas administrativas
@main.route('/admin')
@login_required
@roles_accepted('admin')
def admin():
    datos = {
        'user': current_user,
    }
    return render_template('admin/index.html', datos = datos)

@main.route('/admin/productos')
@login_required
@roles_accepted('admin')
def admin_productos():
    productos = Product.query.all()
    datos = {
        'user': current_user,
        'productos': productos,
    }
    return render_template('admin/productos/index.html', datos = datos)

@main.route('/admin/producto/agregar', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def admin_producto_add():
    if current_user.has_role('admin'):
        form = forms.ProductForm(request.form)
        if request.method == 'POST' :
            img=str(uuid.uuid4())+'.png'
            imagen=request.files['imagen']
            ruta_imagen = os.path.abspath('project\\static\\img')
            imagen.save(os.path.join(ruta_imagen,img)) 
            producto = Product(
                name = form.nombre.data,
                description = form.descripcion.data,
                price = form.precio.data,
                image = img,
                quantity = form.stock.data
            )
            db.session.add(producto)
            db.session.commit()
            flash('Producto creado correctamente')
            return redirect(url_for('main.admin_productos'))
        datos = {
            'form': form,
            'user': current_user,
        }
        return render_template('admin/productos/add.html', datos = datos)
    else:
        return redirect(url_for('main.index'))
    
@main.route('/admin/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def admin_producto_edit(id):
    if current_user.has_role('admin'):
        producto = Product.query.get_or_404(id)
        form = forms.ProductForm(request.form, obj=producto)
        if request.method == 'POST' :
            img=str(uuid.uuid4())+'.png'
            imagen=request.files['imagen']
            ruta_imagen = os.path.abspath('project\\static\\img')
            imagen.save(os.path.join(ruta_imagen,img)) 
            producto.name = form.nombre.data
            producto.description = form.descripcion.data
            producto.price = form.precio.data
            producto.image = img
            producto.quantity = form.stock.data
            db.session.commit()
            flash('Producto editado correctamente')
            return redirect(url_for('main.admin_productos'))
        datos = {
            'form': form,
            'user': current_user,
            'producto': producto
        }
        return render_template('admin/productos/edit.html', datos = datos)
    else:
        return redirect(url_for('main.index'))

@main.route('/admin/productos/eliminar/<int:id>')
@login_required
@roles_accepted('admin')
def admin_producto_delete(id):
    if current_user.has_role('admin'):
        producto = Product.query.get_or_404(id)
        db.session.delete(producto)
        db.session.commit()
        flash('Producto eliminado correctamente')
        return redirect(url_for('main.admin_productos'))
    else:
        return redirect(url_for('main.index'))