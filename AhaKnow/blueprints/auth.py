# -*- coding: utf-8 -*-
"""
    @Author: Zeal Young
    @URL: https://ahaknow.com
    @Create: 2021/9/9 21:07
"""
from flask import Blueprint, render_template, redirect, url_for, flash
# Login and logout
from flask_login import login_user, login_required, logout_user, current_user

from AhaKnow.forms import LoginForm
from AhaKnow.utils import redirect_back
# Login and logout
from AhaKnow.models import Admin

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('Welcome Back.', 'success')
                return redirect_back()
            flash('Is there one missing character in password?', 'warning')
        else:
            flash('Illegal invasion!', 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Farewell.', 'info')
    return redirect_back()
