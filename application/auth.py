import functools
import sys

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from . import login_manager
from application.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if current_user is not None:
        return redirect(url_for('hello'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        error = None

        # Validate the request
        if not name:
            error = 'Name is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'

        if error is None:
            try:
                user = User(
                    name = name,
                    email = email
                )
                user.set_password(password)

                db.session.add(user)
                db.session.commit()
            except RuntimeError as err:
                error = "Error: {0}".format(err)
                pass
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('hello'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None

        user = User.query.filter_by(email=email).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            login_user(user)

            return redirect(url_for('hello'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth.login'))


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login'))
