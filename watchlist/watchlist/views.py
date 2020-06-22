# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
import click
from watchlist import app, db
from watchlist.models import *
from watchlist.ssh_1 import *
import os

# -------------------------------- 教师端 --------------------------------------------#

# index_teacher
@app.route('/index_teacher/', methods=['GET', 'POST'])
# @login_required
def index_teacher():
    courses = Course.query.all()
    relations = Relation.query.filter_by(user_name=current_user.username).all()
    processes = Process.query.all()
    messages = Message.query.all()
    gpus = GPU.query.all()
    return render_template('index_teacher.html', gpus=gpus,courses=courses, processes=processes, messages=messages, relations=relations)

# course_xxx_teacher
@app.route('/my_courses_teacher/<int:id>/', methods=['GET', 'POST'])
@login_required
def course_xxx_teacher(id):
    course = Course.query.filter_by(id=id).first()
    gpus = GPU.query.filter_by(course_name=course.name).first()
    return render_template('course_xxx_teacher.html', course=course,  gpus=gpus)

# my_courses_teacher
@app.route('/my_courses_teacher/', methods=['GET', 'POST'])
# @login_required
def my_courses_teacher():
    courses = Course.query.all()
    relations = Relation.query.filter_by(user_name=current_user.username).all()
    return render_template('my_courses_teacher.html', courses=courses, relations=relations)

# new_courses
@app.route('/new_courses/', methods=['GET', 'POST'])
# @login_required
def new_courses():
    return render_template('new_courses.html')
'''
# GPUs
@app.route('/GPUs/', methods=['GET', 'POST'])
# @login_required
def GPUs():
    return render_template('GPUs.html')'''

# gpu_xxx_teacher
@app.route('/GPUs/<int:id>/', methods=['GET', 'POST'])
@login_required
def gpu_xxx_teacher(id):
    gpus = GPU.query.filter_by(id=id).first()
    processes = Process.query.filter_by(gpu_name=gpus.name).all()
    return render_template('gpu_xxx_teacher.html',gpus=gpus,processes=processes) 

# process_xxx_teacher
@app.route('/process_teacher/<int:id>/', methods=['GET', 'POST'])
# @login_required
def process_xxx_teacher(id):
    process = Process.query.filter_by(id=id).first()
    return render_template('process_xxx_teacher.html',process=process)

# process_teacher
@app.route('/process_teacher/', methods=['GET', 'POST'])
# @login_required
def process_teacher():
    relations = Relation.query.filter_by(user_name=current_user.username).all()
    gpus = GPU.query.all()
    processes = Process.query.all()
    courses = Course.query.all()
    if request.method == 'POST':
        delete_process_id=request.form['delete_process']
        process = Process.query.filter_by(id=delete_process_id).first()
        db.session.delete(process)
        db.session.commit()
        relations = Relation.query.filter_by(user_name=current_user.username).all()
        gpus = GPU.query.all()
        processes = Process.query.all()
        courses = Course.query.all()
        return render_template('process_teacher.html',relations=relations,gpus=gpus,processes=processes,courses=courses)

    return render_template('process_teacher.html',relations=relations,gpus=gpus,processes=processes,courses=courses)

# settings_teacher
@app.route('/settings_teacher/', methods=['GET', 'POST'])
@login_required
def settings_teacher():
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
            return redirect(url_for('settings_teacher'))

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


    return render_template('settings_teacher.html')

#teacher_notice
@app.route('/teacher_notice/', methods=['GET', 'POST'])
# @login_required
def teacher_notice():
    relations = Relation.query.filter_by(user_name=current_user.username).all()
    courses = Course.query.all()
    messages = Message.query.all()
    if request.method == 'POST':
        if 'delete' in request.form.keys():
            delete_id=request.form['delete']
            message = Message.query.filter_by(id=delete_id).first()
            db.session.delete(message)
            db.session.commit()
            relations = Relation.query.filter_by(user_name=current_user.username).all()
            courses = Course.query.all()
            messages = Message.query.all()
            return render_template('teacher_notice.html', relations=relations,courses=courses, messages=messages)
        elif "title" in request.form.keys():
            title=request.form['title']
            edit=request.form['edit']
            course_name=request.form['course']
            message_new = Message(course_name=course_name, title=title, info=edit)
            db.session.add(message_new)
            db.session.commit()
            relations = Relation.query.filter_by(user_name=current_user.username).all()
            courses = Course.query.all()
            messages = Message.query.all()
            return render_template('teacher_notice.html', relations=relations,courses=courses, messages=messages)

    return render_template('teacher_notice.html', relations=relations,courses=courses, messages=messages)

#teacher_notice_xxx
@app.route('/teacher_notice/<int:id>/', methods=['GET', 'POST'])
# @login_required
def teacher_notice_xxx(id):
    message = Message.query.filter_by(id=id).first()
    courses = Course.query.all()
    if request.method == 'POST':
        title=request.form['title']
        edit=request.form['edit']
        message.title=title
        message.info=edit
        db.session.add(message)
        db.session.commit() 
        message = Message.query.filter_by(id=id).first()
        courses = Course.query.all()
        return render_template('teacher_notice_xxx.html', message=message, courses=courses)
    return render_template('teacher_notice_xxx.html', message=message, courses=courses)

#teacher_notice_new
@app.route('/teacher_notice_new/<int:id>/', methods=['GET', 'POST'])
# @login_required
def teacher_notice_new(id):
    course = Course.query.filter_by(id=id).first()
    return render_template('teacher_notice_new.html',course=course)

#teacher_notice_edit
@app.route('/teacher_notice_edit/<int:id>/', methods=['GET', 'POST'])
# @login_required
def teacher_notice_edit(id):
    message = Message.query.filter_by(id=id).first()
    courses = Course.query.all()
    return render_template('teacher_notice_edit.html', message=message, courses=courses)

#course_student
@app.route('/course_student/<int:id>/', methods=['GET', 'POST'])
# @login_required
def course_student(id):
    course = Course.query.filter_by(id=id).first()
    relations = Relation.query.filter_by(course_name=course.name).all()
    relations_stu=[]
    stu_list=[]
    for i in relations:
        if User.query.filter_by(username=i.user_name).first().identity != "teacher":
            relations_stu.append(i)
            stu_list.append(i.user_name)

    if request.method == 'POST':
        import pandas as pd
        import numpy as np
        csv_data = pd.read_csv(request.files['stu_file'])
        print(1)
        csv_list=list(np.array(csv_data))
        for i in range(len(csv_list)):
            if str(csv_list[i][0]) not in stu_list:
                relation = Relation(user_name=str(csv_list[i][0]), course_name=course.name)
                db.session.add(relation)
        db.session.commit()
        course = Course.query.filter_by(id=id).first()
        relations = Relation.query.filter_by(course_name=course.name).all()
        return render_template('course_student.html', course=course, relations=relations_stu)

    return render_template('course_student.html', course=course, relations=relations_stu)

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
                if select == "teacher":
                    return redirect(url_for('index_teacher'))
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
            user = User.query.filter_by(username=username).first()  # 找有没有注册过
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
    messages = Message.query.order_by(Message.id.desc()).all()
    print(messages)
    return render_template('index.html', courses=courses, processes=processes, messages=messages, relations=relations)

# submit
@app.route('/submit/<int:id>/', methods=['GET', 'POST'])
@login_required
def submit(id):
    courses = Course.query.all()
    gpu = GPU.query.filter_by(id=id).first()
    gpuc = GPU_course.query.filter_by(gpu_name=gpu.name).all()
    return render_template('submit.html', courses=courses, gpu=gpu, gpuc=gpuc)

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
    messages = Message.query.order_by(Message.id.desc()).all()
    gpuc = GPU_course.query.filter_by(course_name=course.name).all()

    gpus = GPU.query.all()
    return render_template('course_xxx.html', course=course, messages=messages, gpuc=gpuc, gpus=gpus)

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

# process_xxx_run
# http://127.0.0.1:5000/process/1/run/misaka/test.py/120.78.13.73/22/1314ILYmm/
@app.route('/process/<int:id>/run/<string:user>/<string:file_name>/<string:ip>/<int:port>/<string:password>/', methods=['GET', 'POST'])
@login_required
def process_xxx_run(id,user,file_name,ip,port,password):
    #user = 'misaka'
    #file_name = 'test.py'
    res = docker_test(user,file_name,ip,port,password)
    # 本地存储用户代码输出的文件名
    filename = 'test_tst.txt'
    with open(filename, 'w') as file_object:
        file_object.write(res)

    processes = Process.query.all()
    return render_template('process.html', processes=processes)



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
    messages = Message.query.order_by(Message.id.desc()).all()
    relations = Relation.query.filter_by(user_name=current_user.username).all()
    return render_template('stu_notice.html', courses=courses, messages=messages, relations=relations)

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
         {'name': '深度学习', 'teacher': '梁小丹', 'time': '2017-2018学年 第1学期', 'info': '掌握神经网络框架'},
         {'name': '人工智能原理', 'teacher': '梁小丹', 'time': '2017-2018学年 第1学期', 'info': '实践人工智能项目'},
         {'name': '红楼实验室', 'teacher': '梁小丹', 'time': '2017-2018学年 第1学期', 'info': '学习医学影像分割'},
         {'name': '人工神经网络原理', 'teacher': '姜善成', 'time': '2017-2018学年 第1学期', 'info': '实践人工神经网络项目'},
         {'name': '机器学习', 'teacher': '马倩', 'time': '2017-2018学年 第1学期', 'info': '学习机器学习原理'},
     
     ]
     for c in courses:
         course = Course(name=c['name'], teacher=c['teacher'], time=c['time'], info=c['info'])
         db.session.add(course)
     db.session.commit()


    # 创建进程
     processes = [
         {'name': 'Process 1', 'info': 'simple_1', 'result': '您的计算结果是：1', 'gpu_name': "GPU_1", 'code': 'print(1)', 'state': '正在运行'},
         {'name': 'Process 2', 'info': 'simple_2', 'result': '您的计算结果是：2', 'gpu_name': "GPU_1", 'code': 'print(2)', 'state': '运行完成'},
         {'name': 'Process 3', 'info': 'simple_3', 'result': '您的计算结果是：3', 'gpu_name': "GPU_2", 'code': 'print(3)', 'state': '运行完成'},
         {'name': 'Process 4', 'info': 'simple_4', 'result': '您的计算结果是：4', 'gpu_name': "GPU_3", 'code': 'print(4)', 'state': '正在运行'},
         {'name': 'Process 5', 'info': 'simple_5', 'result': '您的计算结果是：5', 'gpu_name': "GPU_4", 'code': 'print(5)', 'state': '运行完成'},
         {'name': 'Process 6', 'info': 'simple_6', 'result': '您的计算结果是：6', 'gpu_name': "GPU_4", 'code': 'print(6)', 'state': '正在运行'},
         {'name': 'Process 7', 'info': 'simple_7', 'result': '您的计算结果是：7', 'gpu_name': "GPU_5", 'code': 'print(7)', 'state': '运行完成'}
     ]
     for p in processes:
         process = Process(name=p['name'], info=p['info'], result=p['result'], gpu_name=p['gpu_name'], code=p['code'] , state=p['state']  )
         db.session.add(process)
     db.session.commit()

    # 创建消息
     messages = [
         {'course_name': '深度学习', 'title': '作业提交情况', 'info': '甲乙丙丁四个同学没有交作业'},
         {'course_name': '人工智能原理', 'title': '作业提交情况', 'info': '甲乙丙三个同学没有交作业'}, \
         {'course_name': '红楼实验室', 'title': '作业提交情况', 'info': '甲乙两人没有交作业'},

         {'course_name': '深度学习', 'title': '报告上交日期', 'info': '请于5.20前上交报告'},
         {'course_name': '人工智能原理', 'title': '报告上交日期', 'info': '请于5.21前上交报告'},
         {'course_name': '深度学习', 'title': 'GPU可使用时间', 'info': '6月的前两周皆可使用'},

         {'course_name': '红楼实验室', 'title': '报告上交日期', 'info': '请于5.22前上交报告'},
         {'course_name': '人工智能原理', 'title': 'GPU可使用时间', 'info': '7月的前两周皆可使用'},


         {'course_name': '红楼实验室', 'title': 'GPU可使用时间', 'info': '8月的前两周皆可使用'},
     ]
     for m in messages:
         message = Message(course_name=m['course_name'], title=m['title'], info=m['info'])
         db.session.add(message)
     db.session.commit()

    # 创建gpu
     gpus = [
         {'name': 'GPU_1', 'info': '空闲'},
         {'name': 'GPU_2', 'info': '占满'},
         {'name': 'GPU_3', 'info': '占满'},
         {'name': 'GPU_4', 'info': '空闲'},
         {'name': 'GPU_5', 'info': '空闲'}
     ]
     for g in gpus:
         gpu = GPU(name=g['name'], info=g['info'])
         db.session.add(gpu)
     db.session.commit()

    # 创建用户-课程关系
     relations = [
         {'user_name': '17363029', 'course_name': '深度学习'},
         {'user_name': '17363029', 'course_name': '人工智能原理'},
         {'user_name': '17363027', 'course_name': '红楼实验室'},
         {'user_name': '17363027', 'course_name': '机器学习'},
         {'user_name': '梁小丹', 'course_name': '深度学习'},
         {'user_name': '梁小丹', 'course_name': '人工智能原理'},
         {'user_name': '梁小丹', 'course_name': '红楼实验室'},
         {'user_name': '姜善成', 'course_name': '人工神经网络原理'},
         {'user_name': '马倩', 'course_name': '机器学习'},
     ]
     for r in relations:
         relation = Relation(user_name=r['user_name'], course_name=r['course_name'])
         db.session.add(relation)
     db.session.commit()


     # 创建GPU-课程关系
     GPU_courses = [
         {'gpu_name': 'GPU_1', 'course_name': '深度学习'},
         {'gpu_name': 'GPU_2', 'course_name': '人工智能原理'},
         {'gpu_name': 'GPU_3', 'course_name': '机器学习'},
         {'gpu_name': 'GPU_4', 'course_name': '人工智能原理'},
         {'gpu_name': 'GPU_5', 'course_name': '红楼实验室'}
     ]
     for gc in GPU_courses:
         gpu_course = GPU_course(gpu_name=gc['gpu_name'], course_name=gc['course_name'])
         db.session.add(gpu_course)
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