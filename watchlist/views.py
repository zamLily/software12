# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.models import User



# 登录
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username:
            flash('请输入用户名.')
            return redirect(url_for('login'))

        if not password:
            flash('请输入密码.')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()
        if not user:
            flash('用户不存在!')
            return redirect(url_for('login'))

        if user.validate_password(password):
            login_user(user)
            flash('登录成功.')
            return redirect(url_for('index'))
        else:
            flash('密码错误！')
            return redirect(url_for('login'))

    return render_template('login.html')


# 登出
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))


# 注册
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        """Create user."""
        #db.drop_all()   # 想要重置数据库可以用这个
        db.create_all()  # create数据库
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first() # 找有没有注册过
        # user = User.query.first()

        if user is not None:  # 该用户注册过
            flash('User has already existed!')
        else:  # 新用户
            user = User(username=username)
            user.set_password(password)  # 设置密码
            db.session.add(user)
            db.session.commit()  # 提交数据库会话
            flash('Successfully creating user!')
            return redirect(url_for('index'))  # 返回主页

    return render_template('register.html')


#主页
@app.route('/', methods=['GET', 'POST'])
def visitor():
    return render_template('visitor.html')

#主页
@app.route('/index/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')

# my_courses
@app.route('/my_courses/', methods=['GET', 'POST'])
@login_required
def my_courses():
    return render_template('my_courses.html')

# process
@app.route('/process/', methods=['GET', 'POST'])
@login_required
def process():
    return render_template('process.html')

# submit
@app.route('/submit/', methods=['GET', 'POST'])
@login_required
def submit():
    return render_template('submit.html')

# settings
@app.route('/settings/', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')
