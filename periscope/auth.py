from flask import Blueprint, render_template, request
from .models import Employee
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template("login.html")

@auth.route('/admin/em/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            pass
        elif len(password1) < 7:
            pass
        else:
            #add user to database
            new_employee = Employee(email=email, first_name=first_name, last_name=last_name, password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_employee)
            db.session.commit()
            pass

    return render_template("signup.html")