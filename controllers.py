# controllers.py
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User, Boludez

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tacho.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ruta para la página de inicio
@app.route('/')
def home():
    return redirect(url_for('login'))  # Redirige a la página de inicio de sesión

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario registrado con éxito.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Credenciales incorrectas.')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', boludeces=current_user.boludeces)

@app.route('/add_boludez', methods=['POST'])
@login_required
def add_boludez():
    contenido = request.form['contenido']
    privacidad = request.form['privacidad']
    new_boludez = Boludez(contenido=contenido, privacidad=privacidad, owner=current_user)
    db.session.add(new_boludez)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/edit_boludez/<int:boludez_id>', methods=['POST'])
@login_required
def edit_boludez(boludez_id):
    boludez = Boludez.query.get(boludez_id)
    if boludez and boludez.owner == current_user:
        boludez.contenido = request.form['contenido']
        boludez.privacidad = request.form['privacidad']
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/delete_boludez/<int:boludez_id>')
@login_required
def delete_boludez(boludez_id):
    boludez = Boludez.query.get(boludez_id)
    if boludez and boludez.owner == current_user:
        db.session.delete(boludez)
        db.session.commit()
    return redirect(url_for('dashboard'))

# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Cierra la sesión del usuario
    return redirect(url_for('login'))  # Redirige a la página de inicio de sesión