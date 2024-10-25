# from flask import Blueprint, flash, redirect, render_template, request, url_for
# from werkzeug.security import check_password_hash, generate_password_hash
# from flask_login import login_user, login_required, logout_user
# from Lovestock.models import db, User
#
# auth = Blueprint('auth', __name__)
#
#
# @auth.route('/register', methods=('GET', 'POST'))
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#
#         existing_user = User.query.filter_by(username=username).first()
#         if existing_user:
#             flash('Username already exists.')
#             return redirect(url_for('auth.register'))
#
#         hashed_password = generate_password_hash(password, method='sha256')
#         new_user = User(username=username, password=hashed_password)
#
#         db.session.add(new_user)
#         db.session.commit()
#
#         login_user(new_user)
#         return redirect(url_for('stock.index'))
#
#     return render_template('auth/register.html')
#
#
# @auth.route('/login', methods=('GET', 'POST'))
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#
#         user = User.query.filter_by(username=username).first()
#
#         if not user or not check_password_hash(user.password, password):
#             flash('Invalid credentials.')
#             return redirect(url_for('auth.login'))
#
#         login_user(user)
#         return redirect(url_for('stock.index'))
#
#     return render_template('auth/login.html')
#
#
# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('auth.login'))
#
#
#
# # def login_required(view):
# #     @functools.wraps(view)
# #     def wrapped_view(**kwargs):
# #         if g.user is None:
# #             return redirect(url_for('auth.login'))
# #         return view(**kwargs)
# #     return wrapped_view