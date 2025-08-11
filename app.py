import requests


from flask import Flask,flash, render_template, request, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# from models import Category

# Imports para el sistema de login
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
    )



app = Flask(__name__)

app.secret_key = "cualquiercosa"
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mysql+pymysql://root:@localhost/db_miniblog"
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import User, Post, Comment, Category

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from models import User, Post, Comment

@app.route('/')
def index():
    return render_template(
        'index.html'
    )

# SISTEMA DE LOGIN

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] # Pass que llega desde el formulario

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(pwhash=user.password_hash, password=password):
            login_user(user)
            return redirect(url_for('index'))

    return render_template(
        'auth/login.html'
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username exist', 'error')
            return redirect(url_for('register'))
        
        # Hasheo de contraseña
        password_hash = generate_password_hash(
            password=password,
            method='pbkdf2'
        )
        # Creacion del nuevo usuario
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Username created succefully', 'success')
        return redirect(url_for('login'))
    return render_template("auth/register.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# CREAR LAS CATEGORIAS EN LA DB

def cargar_categorias_iniciales():
    categorias = ['Noticias', 'Arte', 'Entretenimiento', 'Videojuegos', 'Historia',
                  'Política', 'Opinión', 'Recomendaciones', 'Reseña', 'Literatura',
                  'Filosofía', 'Ciencia', 'Salud y bienestar', 'Cultura', 'Educación']
    
    for nombre in categorias:
        if not Category.query.filter_by(name=nombre).first():
            db.session.add(Category(name=nombre))
    db.session.commit()

with app.app_context(): # No es lo ideal porque se ejecuta en cada recarga, pero funciona
    if Category.query.count() == 0: # Evita que se ejecute de nuevo la carga completa
        cargar_categorias_iniciales()

# MANEJO DE LAS PAGINAS

@app.context_processor
def get_categories():
    categories = Category.query.all()

    # El context_processor retorna siempre un diccionario, por lo que convertimos los objetos
    # Category del modelo a un diccionario para pasarlo al select y luego al form

    categories_dict = [{'id': c.id, 'name':c.name} for c in categories]
    return dict(categories=categories_dict)

@app.route('/create_post', methods=['GET', 'POST'])


def posts():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        categories_ids = request.form.getlist('categories') # Obtiene una lista de las ids

        if not title or len(title.strip()) == 0:
            flash('El titulo no puede estar vacío.', 'error')
            return redirect(url_for('posts'))

        if not content or len(content.strip()) == 0:
            flash('El post no puede estar vacío.', 'error')
            return redirect(url_for('posts'))

        if len(categories_ids) == 0:
            flash('Debe elegir al menos una categoría para el post.', 'error')
            return redirect(url_for('posts'))
        
        if len(categories_ids) > 3:
            flash('Solo puede elegir un máximo de 3 categorías')
            return redirect(url_for('posts'))
        
        categories = Category.query.filter(Category.id.in_(categories_ids)).all()
        for cat in categories:
            print(cat.name)

        new_post = Post(
            title=title,
            content=content,
            user_id=current_user.id
        )

        # Convierte las id recibidas por el formulario en objetos Category y los
        # agrega al post (SQLAlchemy carga los datos en la tabla intermedia)
        categories = Category.query.filter(Category.id.in_(categories_ids)).all()
        new_post.categories = categories

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('posts'))

    #verificar que exista algun post
    existingPosts = Post.query.order_by(Post.date.desc()).all()
    return render_template(
        'create_post.html',
        existingPosts=existingPosts
    )

#borrado logico de post
@app.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id, is_active=1).first_or_404(description="Posteo no encontrado o ya está desactivado")

    if post.user_id == current_user.id:
        post.is_active = 0
        db.session.commit()
        flash("Post eliminado correctamente", "success")
    else:
        flash("No puedes eliminar este Post", "error")


    return redirect(url_for('posts'))


@app.route('/edit_post/<int:post_id>' , methods=['GET', 'POST'])
@login_required
def edit_post(post_id): 
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']

        if new_title == post.title and new_content == post.content:
            flash('No se realizaron cambios en el post', 'info')
        else:
            post.title = new_title
            post.content = new_content
            db.session.commit()
            flash('Post editado correctamente', 'success')
            
        
        
        return redirect(url_for('posts'))

    return render_template('edit_post.html', post=post)

@app.route('/post/<int:post_id>/comment', methods = ['POST'])
@login_required
def create_comment(post_id):

        if request.method == 'POST':
            post = Post.query.get_or_404(post_id)
            content = request.form['content']
            if not content or len(content.strip()) == 0:
                flash('El comentario no puede estar vacío.', 'error')
                return redirect(url_for('posts', _anchor=f'post-{post_id}'))
            
            comment = Comment(
                content=content,
                user_id=current_user.id,
                post_id=post_id,
                is_active=True
            )

        db.session.add(comment)
        db.session.commit()

        flash('Comentario agregado exitosamente.', 'success')

        return redirect(url_for('posts', _anchor=f'post-{post_id}'))

if __name__ == '__main__':
    app.run(debug=True)