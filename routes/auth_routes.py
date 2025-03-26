import logging
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from models import User
from forms import LoginForm, SignupForm
from app import db

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        logger.debug(f"Login attempt for email: {form.email.data}")
        
        if user:
            logger.debug(f"User found: {user.username}, Admin: {user.is_admin}")
            password_check = user.check_password(form.password.data)
            logger.debug(f"Password check result: {password_check}")
            
            if password_check:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                
                if user.is_admin:
                    logger.debug(f"Admin user logged in, redirecting to dashboard")
                    return redirect(next_page or url_for('admin.dashboard'))
                else:
                    logger.debug(f"Regular user logged in, redirecting to index")
                    return redirect(next_page or url_for('main.index'))
            else:
                flash('Login failed. Please check your password.', 'danger')
        else:
            flash('Login failed. No user found with that email.', 'danger')
    
    return render_template('login.html', form=form)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = SignupForm()
    
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('signup.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
