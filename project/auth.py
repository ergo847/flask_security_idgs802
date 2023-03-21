from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import User
from . import db, userDataStore

auth = Blueprint('auth', __name__, url_prefix='/security')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('El usuario y/o contraseña son incorrectos.')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        return redirect(url_for('main.index'))

    elif request.method == 'GET':
        return render_template('/security/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()

        if user:
            flash('El correo ya esta en uso.')
            return redirect(url_for('auth.register'))
        
        userDataStore.create_user(name = name, email = email, password = generate_password_hash(password, method='sha256'))

        db.session.commit()
        return redirect(url_for('auth.login'))
    elif request.method == 'GET':
        return render_template('/security/register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

