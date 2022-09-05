"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'watercolor123454321'
app.config['SQLALCHEMY_ECHO'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def root():
    """Homepage redirects to user homepage with users list"""
    
    return redirect('/users')

@app.errorhandler(404)
def page_not_found(e):
    """404 for not found page"""
    return render_template('404.html')

#########################USER ROUTE
@app.route('/users')
def users_index():
    """ shows page with all users listed"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def users_new_form():
    """ Shows new user creation form"""
    return render_template('users/new.html')

@app.route('/users/new', methods=["POST"])
def users_new():
    """Handle sent new user form and create new user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added.")

    return redirect('/users')


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Shows specific user page based on user id"""

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Shows for to edit existing user details"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_upade(user_id):
    """Handles form submission for updating existing user info"""

    user = User.query.get_or_404(user_id)
    user.first_name=request.form['first_name'],
    user.last_name=request.form['last_name'],
    user.image_url=request.form['image_url']

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_delete(user_id):
    """Handle form deletion for existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {new_user.full_name} deleted.")

    return redirect('/users')


######POSTS ROUTES

@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Form to create new post for user"""
    
    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user= user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new_form(user_id):
    """Form sumbmission from user post form"""
    user = User.query.get_or_404(user_id)
    new_post = Post(title = request.form['title'],
        content = request.form['content'],
        user = user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")    

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Shows a specific post"""
    
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post = post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Shows a form for user to edit post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post = post)


@app.route('/posts/<int:post_id>/edit', methods = ["POST"])
def posts_edit(post_id):
    """Handle form submission to edit a post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.sesion.commit()

    flash(f"Post '{post.title}' edited.")

    return redirect(f'/users/{post.user_id}')


@app.route('/posts/<int:post_id>/delete', methods = ["POST"])
def posts_edit(post_id):
    """Handle form submission for deleting a post"""


    db.session.delete(post)
    db.sesion.commit()

    flash(f"Post '{post.title}' deleted.")

    return redirect(f'/users/{post.user_id}')
    


    
