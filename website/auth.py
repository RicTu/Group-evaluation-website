from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import pandas as pd

students_csv = pd.read_csv("./website/student_list.csv",encoding="utf_8_sig")
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        StudentID = request.form.get('StudentID').upper()
        password = request.form.get('password')


        user = User.query.filter_by(StudentID=StudentID).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                if StudentID == "NORDLINGLAB":
                    return redirect(url_for('views.admin'))
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Invalid student ID or you didn\'t sign up.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        StudentID = request.form.get('StudentID').upper()
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(StudentID=StudentID).first()
        if user:
            flash('Account already exists.', category='error')
        elif StudentID not in list(students_csv["ID"]):
            flash('Invalid student ID.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 5:
            flash('Password must be at least 7 characters.', category='error')
        else:
            idx_csv = students_csv.index[students_csv["ID"]==StudentID].tolist()[0]
            group = int(students_csv.loc[students_csv["ID"]==StudentID]["Group"])
            group_member = list(students_csv.loc[students_csv['Group'] == group]["Name"])
            new_user = User(StudentID=StudentID, password=generate_password_hash(
            password1, method='sha256'), group=group, idx_csv=idx_csv)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            if StudentID == "NORDLINGLAB":
                    return redirect(url_for('views.admin'))
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
