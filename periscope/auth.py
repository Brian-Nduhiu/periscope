import re
from flask import Blueprint, render_template, request, redirect, url_for
from .models import Employee
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask_login import login_user,login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    logged = False
    correct_password = True
    correct_email = True
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        employee = Employee.query.filter_by(email=email).first()
        if employee:
            if check_password_hash(employee.password, password):
                logged = True
                login_user(employee, remember=True)
                return redirect(url_for('views.home'))
            else:
                correct_password = False
        else:
            correct_email = False


    return render_template("login.html",logged=logged, correct_password=correct_password, correct_email=correct_email)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/admin/em/signup', methods=['GET', 'POST'])
def signup():
    
    flash = False
    em_exists = False
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        

        employee = Employee.query.filter_by(email=email).first()

        if  employee:
            em_exists = True
        elif password1 != password2:
            flash = True
        elif len(password1) < 7:
            flash = True
        else:
            #add user to database
            new_employee = Employee(email=email, first_name=first_name, last_name=last_name, password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_employee)
            db.session.commit()
            return redirect(url_for('auth.login'))

    return render_template("signup.html", flash=flash, em_exists=em_exists)