# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
import click
from watchlist import app, db
from watchlist.models import *
import os

# -------------------------------- 教师端 --------------------------------------------#

# index_teacher
@app.route('/index_teacher/', methods=['GET', 'POST'])
# @login_required
def index_teacher():
    return render_template('index_teacher.html')

# course_xxx_teacher
@app.route('/my_courses_teacher/<int:id>/', methods=['GET', 'POST'])
@login_required
def course_xxx_teacher(id):
    course = Course.query.filter_by(id=id).first()
    messages = Message.query.all()
    gpus = GPU.query.all()
    return render_template('course_xxx_teacher.html', course=course, messages=messages, gpus=gpus)


# my_courses_teacher
@app.route('/my_courses_teacher/', methods=['GET', 'POST'])
# @login_required
def my_courses_teacher():
    return render_template('my_courses_teacher.html')

# gpu_xxx_teacher
@app.route('/gpu_xxx_teacher/', methods=['GET', 'POST'])
# @login_required
def gpu_xxx_teacher():
    return render_template('gpu_xxx_teacher.html')

# -------------------------------- 学生端 --------------------------------------------#

# 登录
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        select = request.form['certification']

        if not username:
            flash('请输入用户名.')
            return redirect(url_for('login'))

        if not password:
            flash('请输入密码.')
            return redirect(url_for('login'))

        if select == "请选择":
            flash("请选择 学生or老师")

        else:
            user = User.query.filter_by(username=username, identity=select).first()
            if not user:
                flash('用户不存在!')
                return redirect(url_for('login'))

            if user.validate_password(password):
                login_user(user)
                flash('登录成功！')
                print(current_user.username)
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
    return redirect(url_for('visitor'))


# 注册
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        """Create user."""
        username = request.form['username']
        password = request.form['password']

        select = request.form['certification']

        if select == "请选择":
            flash("请选择 学生or老师")

        else:
            user = User.query.filter_by(username=username, identity=select).first()  # 找有没有注册过
            # user = User.query.first()

            if user is not None:  # 该用户注册过
                flash('用户已经存在！')

            else:  # 新用户
                user = User(username=username, identity=select)
                user.set_password(password)  # 设置密码
                db.session.add(user)
                db.session.commit()  # 提交数据库会话
                flash('成功注册！')
                return redirect(url_for('visitor'))  # 返回主页

            #flash(select)
            #db.drop_all()   # 想要重置数据库可以用这个
            #db.create_all()  # create数据库

    return render_template('signup.html')


#主页
@app.route('/', methods=['GET', 'POST'])
def visitor():
    return render_template('visitor.html')

#主页
@app.route('/index/', methods=['GET', 'POST'])
@login_required
def index():
    courses = Course.query.all()
    relations = Relation.query.filter_by(user_name=current_user.username).all()
    processes = Process.query.all()
    messages = Message.query.all()
    return render_template('index.html', courses=courses, processes=processes, messages=messages, relations=relations)

# submit
@app.route('/submit/<int:id>/', methods=['GET', 'POST'])
@login_required
def submit(id):
    courses = Course.query.all()
    gpu = GPU.query.filter_by(id=id).first()
    return render_template('submit.html', courses=courses, gpu=gpu)

# settings
@app.route('/settings/', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        button_name = request.form['submit_name']
        if button_name == "确定":
            img = request.files.get('upload_img')
            basepath = os.path.dirname(__file__)
            file_path = os.path.join(basepath, 'static/photo', img.filename)
            #path = "/static/photo/"
            #file_path = path + img.filename
            img.save(file_path)
            pic_path = os.path.join('/static/photo', img.filename)
            current_user.pic_path = pic_path
            db.session.add(current_user)
            db.session.commit()  # 提交数据库会话

        if button_name == "取消":
            return redirect(url_for('settings'))

        if button_name == "更改名称":
            new_name = request.form['newname']
            user = User.query.filter_by(username=new_name).first()  # 找有没有注册过
            # user = User.query.first()

            if user is not None:  # 该用户注册过
                flash('该用户名已被占用！')
            else:
                current_user.username = new_name
                db.session.add(current_user)
                db.session.commit()  # 提交数据库会话

        if button_name == "更改密码":
            new_password = request.form['newpw']
            current_user.set_password(new_password)  # 设置密码
            db.session.add(current_user)
            db.session.commit()  # 提交数据库会话

        if button_name == "更改学号":
            newstuid = request.form['newstuid']
            current_user.stu_id = newstuid
            db.session.add(current_user)
            db.session.commit()  # 提交数据库会话

        if button_name == "更改年级":
            newgrade = request.form['newgrade']
            current_user.ingrade = newgrade
            db.session.add(current_user)
            db.session.commit()  # 提交数据库会话

        if button_name == "更改班级":
            newclass = request.form['newclass']
            current_user.inclass = newclass
            db.session.add(current_user)
            db.session.commit()  # 提交数据库会话

    return render_template('settings.html')

# my_courses
@app.route('/my_courses/', methods=['GET', 'POST'])
@login_required
def my_courses():
    courses = Course.query.all()
    relations = Relation.query.filter_by(user_name=current_user.username).all()
    return render_template('my_courses.html', courses=courses, relations=relations)

# all_courses
@app.route('/my_courses/all_courses/', methods=['GET', 'POST'])
@login_required
def all_courses():
    courses = Course.query.all()
    return render_template('all_courses.html', courses=courses)

# course_xxx
@app.route('/my_courses/all_courses/<int:id>/', methods=['GET', 'POST'])
@login_required
def course_xxx(id):
    course = Course.query.filter_by(id=id).first()
    messages = Message.query.all()
    gpus = GPU.query.all()
    return render_template('course_xxx.html', course=course, messages=messages, gpus=gpus)

# process
@app.route('/process/', methods=['GET', 'POST'])
@login_required
def process():
    processes = Process.query.all()
    return render_template('process.html', processes=processes)

# process_xxx
@app.route('/process/<int:id>/', methods=['GET', 'POST'])
@login_required
def process_xxx(id):
    process = Process.query.filter_by(id=id).first()
    return render_template('process_xxx.html', process=process)

# process_edit
@app.route('/process_edit/<int:id>/', methods=['GET', 'POST'])
@login_required
def process_edit(id):
    process = Process.query.filter_by(id=id).first()
    return render_template('process_edit.html', process=process)


# stu_notice
@app.route('/message/', methods=['GET', 'POST'])
@login_required
def stu_notice():
    courses = Course.query.all()
    messages = Message.query.all()
    return render_template('stu_notice.html', courses=courses, messages=messages)

# stu_notice_xxx
@app.route('/message/<int:id>/', methods=['GET', 'POST'])
@login_required
def stu_notice_xxx(id):
    message = Message.query.filter_by(id=id).first()
    courses = Course.query.all()
    return render_template('stu_notice_xxx.html', message=message, courses=courses)



@app.cli.command()
def forge():
     # Generate fake data.
     #db.create_all()

     # 创建课程
     courses = [
         {'name': '程序设计基础', 'teacher': '谭光', 'time': '2017-2018学年 第1学期', 'info': 'xxx'},
         {'name': '人工智能原理', 'teacher': '梁小丹', 'time': '2017-2018学年 第1学期', 'info': 'xxx'},
         {'name': 'xxx实验室', 'teacher': 'xxx', 'time': 'xxx学年 第xx学期', 'info': 'xxx'}
     ]
     for c in courses:
         course = Course(name=c['name'], teacher=c['teacher'], time=c['time'], info=c['info'])
         db.session.add(course)
     db.session.commit()


    # 创建进程
     processes = [
         {'name': 'Process 1', 'info': 'xxx', 'result': 'xxxxxxx', 'gpu_name': "GPU_1", 'code': 'print(1)', 'state': '正在运行'},
         {'name': 'Process 2', 'info': 'xxx', 'result': 'xxxxxxx', 'gpu_name': "GPU_1", 'code': 'print(2)', 'state': '运行完成'},
         {'name': 'Process 3', 'info': 'xxx', 'result': 'xxxxxxx', 'gpu_name': "GPU_2", 'code': 'print(3)', 'state': '运行完成'},
         {'name': 'Process 4', 'info': 'xxx', 'result': 'xxxxxxx', 'gpu_name': "GPU_3", 'code': 'print(4)', 'state': '正在运行'},
         {'name': 'Process 5', 'info': 'xxx', 'result': 'xxxxxxx', 'gpu_name': "GPU_4", 'code': 'print(5)', 'state': '运行完成'},
         {'name': 'Process 6', 'info': 'xxx', 'result': 'xxxxxxx', 'gpu_name': "GPU_4", 'code': 'print(6)', 'state': '正在运行'},
         {'name': 'Process 7', 'info': 'xxx', 'result': 'xxxxxxx', 'gpu_name': "GPU_5", 'code': 'print(7)', 'state': '运行完成'}
     ]
     for p in processes:
         process = Process(name=p['name'], info=p['info'], result=p['result'], gpu_name=p['gpu_name'], code=p['code'] , state=p['state']  )
         db.session.add(process)
     db.session.commit()

    # 创建消息
     messages = [
         {'course_name': '程序设计基础', 'title': '作业提交情况', 'info': '甲乙丙丁四个同学没有交作业'},
         {'course_name': '程序设计基础', 'title': '报告上交日期', 'info': '请于5.20前上交报告'},
         {'course_name': '程序设计基础', 'title': 'GPU可使用时间', 'info': '6月的前两周皆可使用'},

         {'course_name': '人工智能原理', 'title': '作业提交情况', 'info': '甲乙丙丁四个同学没有交作业'},
         {'course_name': '人工智能原理', 'title': '报告上交日期', 'info': '请于5.20前上交报告'},
         {'course_name': '人工智能原理', 'title': 'GPU可使用时间', 'info': '6月的前两周皆可使用'},

         {'course_name': 'xxx实验室', 'title': '作业提交情况', 'info': '甲乙丙丁四个同学没有交作业'},
         {'course_name': 'xxx实验室', 'title': '报告上交日期', 'info': '请于5.20前上交报告'},
         {'course_name': 'xxx实验室', 'title': 'GPU可使用时间', 'info': '6月的前两周皆可使用'},
     ]
     for m in messages:
         message = Message(course_name=m['course_name'], title=m['title'], info=m['info'])
         db.session.add(message)
     db.session.commit()

    # 创建gpu
     gpus = [
         {'name': 'GPU_1', 'info': '空闲', 'course_name': '程序设计基础'},
         {'name': 'GPU_2', 'info': '占满', 'course_name': '人工智能原理'},
         {'name': 'GPU_3', 'info': '占满', 'course_name': '程序设计基础'},
         {'name': 'GPU_4', 'info': '空闲', 'course_name': '人工智能原理'},
         {'name': 'GPU_5', 'info': '空闲', 'course_name': 'xxx实验室'}
     ]
     for g in gpus:
         gpu = GPU(name=g['name'], info=g['info'], course_name=g['course_name'])
         db.session.add(gpu)
     db.session.commit()

    # 创建关系
     relations = [
         {'user_name': '1', 'course_name': '程序设计基础'},
         {'user_name': '1', 'course_name': '人工智能原理'},
         {'user_name': '1', 'course_name': 'xxx实验室'},
         {'user_name': '2', 'course_name': '程序设计基础'},
         {'user_name': '2', 'course_name': '人工智能原理'},
         {'user_name': '3', 'course_name': '程序设计基础'}
     ]
     for r in relations:
         relation = Relation(user_name=r['user_name'], course_name=r['course_name'])
         db.session.add(relation)
     db.session.commit()


"""
@app.cli.command()
def forgep():
     # Generate fake data.
     #db.create_all()

     processes = [
         {'name': 'Process 1', 'info': 'xxx', 'result': 'xxxxxxx', 'gpu_name': "GPU_1"},
         {'name': 'Process 2', 'info': 'xxx', 'result': 'xxxxxxx', 'gpu_name': "GPU_1"},
         {'name': 'Process 3', 'info': 'xxx', 'result': 'xxxxxxx', 'gpu_name': "GPU_2"},
         {'name': 'Process 4', 'info': 'xxx', 'result': 'xxxxxxx', 'gpu_name': "GPU_3"},
         {'name': 'Process 5', 'info': 'xxx', 'result': 'xxxxxxx', 'gpu_name': "GPU_4"},
         {'name': 'Process 6', 'info': 'xxx', 'result': 'xxxxxxx', 'gpu_name': "GPU_4"},
         {'name': 'Process 7', 'info': 'xxx', 'result': 'xxxxxxx', 'gpu_name': "GPU_5"}
     ]
     for p in processes:
         process = Process(name=p['name'], info=p['info'], result=p['result'], gpu_name=p['gpu_name'] )
         db.session.add(process)
     db.session.commit()




@app.cli.command()
def forgem():
     # Generate fake data.
     #db.create_all()

     messages = [
         {'course_name': '程序设计基础', 'title': '作业提交情况', 'info': '甲乙丙丁四个同学没有交作业'},
         {'course_name': '程序设计基础', 'title': '报告上交日期', 'info': '请于5.20前上交报告'},
         {'course_name': '程序设计基础', 'title': 'GPU可使用时间', 'info': '6月的前两周皆可使用'},

         {'course_name': '人工智能原理', 'title': '作业提交情况', 'info': '甲乙丙丁四个同学没有交作业'},
         {'course_name': '人工智能原理', 'title': '报告上交日期', 'info': '请于5.20前上交报告'},
         {'course_name': '人工智能原理', 'title': 'GPU可使用时间', 'info': '6月的前两周皆可使用'},

         {'course_name': 'xxx实验室', 'title': '作业提交情况', 'info': '甲乙丙丁四个同学没有交作业'},
         {'course_name': 'xxx实验室', 'title': '报告上交日期', 'info': '请于5.20前上交报告'},
         {'course_name': 'xxx实验室', 'title': 'GPU可使用时间', 'info': '6月的前两周皆可使用'},
     ]
     for m in messages:
         message = Message(course_name=m['course_name'], title=m['title'], info=m['info'])
         db.session.add(message)
     db.session.commit()


@app.cli.command()
def forgeg():
     # Generate fake data.
     #db.create_all()

     gpus = [
         {'name': 'GPU_1', 'info': '空闲', 'course_name': '程序设计基础'},
         {'name': 'GPU_2', 'info': '占满', 'course_name': '人工智能原理'},
         {'name': 'GPU_3', 'info': '占满', 'course_name': '程序设计基础'},
         {'name': 'GPU_4', 'info': '空闲', 'course_name': '人工智能原理'},
         {'name': 'GPU_5', 'info': '空闲', 'course_name': 'xxx实验室'}
     ]
     for g in gpus:
         gpu = GPU(name=g['name'], info=g['info'], course_name=g['course_name'])
         db.session.add(gpu)
     db.session.commit()


@app.cli.command()
def forger():
     # Generate fake data.
     #db.create_all()

     relations = [
         {'user_name': '1', 'course_name': '程序设计基础'},
         {'user_name': '1', 'course_name': '人工智能原理'},
         {'user_name': '1', 'course_name': 'xxx实验室'},
         {'user_name': '2', 'course_name': '程序设计基础'},
         {'user_name': '2', 'course_name': '人工智能原理'},
         {'user_name': '3', 'course_name': '程序设计基础'}
     ]
     for r in relations:
         relation = Relation(user_name=r['user_name'], course_name=r['course_name'])
         db.session.add(relation)
     db.session.commit()
"""