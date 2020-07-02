# -*- coding: utf-8 -*-
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from watchlist import db


# 用户table
class User(db.Model, UserMixin):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)                        # id（主键）

    username = db.Column(db.String(20))                                 # 用户名
    password_hash = db.Column(db.String(128))                           # 用户密码
    identity = db.Column(db.String(128))                                # 身份：学生or老师

    pic_path = db.Column(db.String(128), default="/static/pic/1.jpg")   # 用户头像地址
    stu_id = db.Column(db.String(20), default="未填写")                  # 学生学号
    ingrade = db.Column(db.String(20), default="未填写")                 # 学生年级
    inclass = db.Column(db.String(20), default="未填写")                 # 学生年班级

    def set_password(self, password):       # 将用户密码进行hash加密
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):  # 登录时验证用户输入的密码是否正确
        return check_password_hash(self.password_hash, password)

    def validate_identity(self, identity):  # 验证登录的用户身份（学生/老师）
        return identity == self.identity


# 课程表table
class Course(db.Model):
    __tablename__ = 'Course'

    id = db.Column(db.Integer, primary_key=True)  # id（主键）
    name = db.Column(db.String(50))               # 课程名称
    teacher = db.Column(db.String(50))            # 任课老师
    time = db.Column(db.String(50))               # 授课时间（学年、学期）
    info = db.Column(db.String(300))              # 课程其他信息
    course_name = db.Column(db.String(50), db.ForeignKey('Course.name'))  # 用户对应的课程
    gpu_name = db.Column(db.String(50), db.ForeignKey('GPU.name'))  # gpu name
    pic_path = db.Column(db.String(128), default="/static/pic/course_logo.png")  # 课程头像


# 用户-课程-gpu-使用量-最后使用时间 关系table
class Usage(db.Model):
    __tablename__ = 'Usage'

    id = db.Column(db.Integer, primary_key=True)  # id（主键）
    user_name = db.Column(db.String(50), db.ForeignKey('User.username'))  # 用户名
    course_name = db.Column(db.String(50), db.ForeignKey('Course.name'))  # 进程对应的课程
    gpu_name = db.Column(db.String(50), db.ForeignKey('GPU.name'))  # gpu name
    submit_num = db.Column(db.Integer, default=0)  # 总提交进程数
    last_time = db.Column(db.DateTime, default=datetime.utcnow)  # 最后一次提交进程的时间


# 用户-课程关系table
class Relation(db.Model):
    __tablename__ = 'Relation'

    id = db.Column(db.Integer, primary_key=True)                          # id（主键）
    user_name = db.Column(db.String(50), db.ForeignKey('User.username'))  # 存储用户名
    course_name = db.Column(db.String(50), db.ForeignKey('Course.name'))  # 用户对应的课程

class GPU_course(db.Model):
    __tablename__ = 'GPU_course'

    id = db.Column(db.Integer, primary_key=True)  # id（主键）
    gpu_name = db.Column(db.String(50), db.ForeignKey('GPU.name'))        # gpu name
    course_name = db.Column(db.String(50), db.ForeignKey('Course.name'))  # 用户对应的课程

class Process_stu(db.Model):
    __tablename__ = 'Process_stu'

    id = db.Column(db.Integer, primary_key=True)  # id（主键）
    user_name = db.Column(db.String(50), db.ForeignKey('User.username'))  # 存储用户名
    process_name = db.Column(db.String(50), db.ForeignKey('Process.name'))  # 程序的名称




# 程序table
class Process(db.Model):
    __tablename__ = 'Process'

    id = db.Column(db.Integer, primary_key=True)                    # id（主键）
    name = db.Column(db.String(50))                                 # 程序的名称
    info = db.Column(db.String(300))                                # 程序的信息
    state = db.Column(db.String(50))                                # 是否运行完成
    result = db.Column(db.String(1000))                             # 程序的结果
    code = db.Column(db.String(10000))                              # 存储代码，方便以后编辑代码
    course_name = db.Column(db.String(50), db.ForeignKey('Course.name'))  # 程序所属的课程
    gpu_name = db.Column(db.String(50), db.ForeignKey('GPU.name'))  # 程序在哪个gpu上跑的

# 消息table
class Message(db.Model):
    __tablename__ = 'Message'

    id = db.Column(db.Integer, primary_key=True)                           # id（主键）
    course_name = db.Column(db.String(50), db.ForeignKey('Course.name'))   # 消息对应的课程
    title = db.Column(db.String(50))                                       # 消息的标题
    info = db.Column(db.String(1000))                                      # 消息的内容


# GPU table
class GPU(db.Model):
    __tablename__ = 'GPU'

    id = db.Column(db.Integer, primary_key=True)    # id（主键）
    name = db.Column(db.String(30))                 # gpu的名称
    info = db.Column(db.String(1000))               # gpu是否空闲

    # 配置和操作需要使用的参数
    ip = db.Column(db.String(20))                  # ip
    port = db.Column(db.Integer)                 # port
    username = db.Column(db.String(40))             # username
    password = db.Column(db.String(40))             # password
"""
class Student(db.Model, UserMixin):
    __tablename__ = 'origin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    ingrade = db.Column(db.String(20))
    inclass = db.Column(db.String(20))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Teacher(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

"""

