from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, jsonify
from . import db
from .models import User, Img
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, logout_user, current_user
from displayTumor import *
from predictTumor import predictTumor
import cv2

DT = object()
auth = Blueprint('auth', __name__)

def tumor(img):
    DT = DisplayTumor()
    print(img)
    img = cv2.imread(img)
    DT.readImage(img)
    DT.removeNoise()
    DT.displayTumor()
    return DT.curImg

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        print(data)
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signUp', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template('signUp.html', user = current_user)

@auth.route('/upload', methods = ['POST'])
def upload():
    pic = request.files['img']
    if not pic:
        flash('No file selected!', category='error')
        return render_template("home.html", user=current_user)
    # filename = secure_filename(pic.filename)
    # mimetype = pic.mimetype
    # img = Img(img = pic.read(), mimetype = mimetype, name = filename)
    # db.session.add(img)
    # db.session.commit()
    pic.save('website/static/file.jpg')
    coloured_pic = tumor("website/static/file.jpg")
    cv2.imwrite('website/static/processed_file.jpg',coloured_pic)
    print('Image has been uploaded!')
    return render_template('upload.html', user = current_user)

@auth.route('/check', methods = ['GET', 'POST'])
def check():
    img = cv2.imread("website/static/file.jpg")
    print(img)
    val = predictTumor(img)
    if val == 1:
        res = "Brain Tumor is present"
    else:
        res = "There is no sign of Tumor"
    return jsonify({'string_value': res})

