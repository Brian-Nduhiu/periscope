from flask import Blueprint, render_template, request

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
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            pass
        elif len(password1) < 7:
            pass
        else:
            #add user to database
            pass

    return render_template("signup.html")