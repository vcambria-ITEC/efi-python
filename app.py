import requests

from flask import Flask,flash, render_template, request, redirect, url_for
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models import (
    db,
    Post,
    Comment,
    Category
)
from views import (
    UserAPI,
    UserDetailAPI,
    UserRegisterAPI,
    LoginAPI
)

app = Flask(__name__)

app.secret_key = "cualquiercosa"
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mysql+pymysql://root:@localhost/db_miniblog"
)

app.config['JWT_SECRET_KEY'] = 'cualquier-cosa'
jwt = JWTManager(app)

db.init_app(app)
migrate = Migrate(app, db)

app.add_url_rule(
    '/api/register',
    view_func=UserRegisterAPI.as_view('register_api'),
    methods=['POST']
)

app.add_url_rule(
    '/api/login',
    view_func=LoginAPI.as_view('login'),
    methods=['POST']
)

@app.route('/')
def index():
    return render_template(
        'index.html'
    )


""" 
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
        new_categories_ids = request.form.getlist('categories')
        new_categories = Category.query.filter(Category.id.in_(new_categories_ids)).all()

        # Validacion para que no quede un post sin categorizar
        if new_title == post.title and new_content == post.content and post.categories == new_categories:
            flash('No se realizaron cambios en el post', 'info')
        else:

            if len(new_categories_ids) == 0:
                flash('Debe elegir al menos una categoría para el post.', 'error')
                return redirect(url_for('edit_post',post_id=post_id))

            post.title = new_title
            post.content = new_content
            post.categories = new_categories
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
 """
if __name__ == '__main__':
    app.run(debug=True)