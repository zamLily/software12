# -*- coding: utf-8 -*-
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from watchlist import db


class User(db.Model, UserMixin):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    identity = db.Column(db.String(128))

    ingrade = db.Column(db.String(20))
    inclass = db.Column(db.String(20))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def validate_identity(self, identity):
        return identity == self.identity


class Course(db.Model):
    __tablename__ = 'Course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    teacher = db.Column(db.String(50))
    time = db.Column(db.String(50))
    info = db.Column(db.String(300))
    message = db.Column(db.String(300))
    istaken = db.Column(db.Boolean, default=False)


class Process(db.Model):
    __tablename__ = 'Process'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))  # 程序的名称
    info = db.Column(db.String(300))  # 程序的信息
    result = db.Column(db.String(1000))  # 程序的结果
    code = db.Column(db.String(10000))  # 存储代码，方便以后编辑代码
    gpu_name = db.Column(db.String(50), db.ForeignKey('GPU.name'))  # 程序在哪个gpu上跑的


class Message(db.Model):
    __tablename__ = 'Message'

    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(50), db.ForeignKey('Course.name'))  # 消息对应的课程
    title = db.Column(db.String(50))   # 消息的标题
    info = db.Column(db.String(1000))  # 消息的内容

class GPU(db.Model):
    __tablename__ = 'GPU'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50)) # gpu的名称
    info = db.Column(db.String(1000))  # gpu是否空闲
    course_name = db.Column(db.String(50), db.ForeignKey('Course.name')) # gpu对应的课程

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

