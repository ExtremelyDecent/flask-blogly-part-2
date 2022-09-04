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

    
@app.errorhandler(404)
def page_not_found(e):
    """404 for not found page"""
    return render_template('404.html')


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

    return redirect('/users')

