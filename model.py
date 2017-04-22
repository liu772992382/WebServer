# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer, SmallInteger, String, Table, Text, \
                       text, create_engine, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask import Flask
from config import *
import sys, os
import time
import logging

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker()
Session.configure(bind=engine)
Base = declarative_base()
session = Session()

def get_time():
    return time.strftime("%Y-%m-%d %X", time.localtime())



class User(Base):
    __tablename__ = 'users'

    uid = Column(Integer, primary_key=True) #用户编号
    openId = Column(String(255))    #微信openId
    nickName = Column(String(255))  #昵称
    gender = Column(Integer)    #性别
    type = Column(Integer)  #用户类型，具体类型待定
    loginTime = Column(String(255)) #用户上次登陆时间
    avatarUrl = Column(String(255))    #用户头像链接
    city = Column(String(255))  #所在城市
    createTime = Column(String(255))    #用户创建时间

    def init_user(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__



class Activity(Base):
    __tablename__ = 'activities'

    aid = Column(Integer, primary_key=True) #活动编号
    name = Column(String(255))  #活动名
    organizer = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)  #活动组织者
    time = Column(String(255))  #活动时间
    content = Column(String(5000))   #活动内容
    summary = Column(String(255))   #活动概要
    createTime = Column(String(255))    #活动创建时间
    cover = Column(String(255)) #封面图片的文件名
    location = Column(String(255))  #活动地址
    state = Column(Integer) #活动状态,1为正在进行，0为结束


    user = relationship(u'User')

    def init_activity(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__


class ActivityImage(Base):
    __tablename__ = 'activity_image'

    aimid = Column(Integer, primary_key=True)
    md5 = Column(String(255))
    aid = Column(ForeignKey(u'activities.aid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)   #参与者参与的活动

    activity = relationship(u'Activity')

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__

class Participant(Base):
    __tablename__ = 'participants'

    pid = Column(Integer, primary_key=True) #活动参与者编号
    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #参与者对应的用户编号
    aid = Column(ForeignKey(u'activities.aid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)   #参与者参与的活动
    time = Column(String(255))  #参与的时间

    user = relationship(u'User')
    activity = relationship(u'Activity')

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__

class Moment(Base):
    __tablename__ = 'moments'

    mid = Column(Integer, primary_key=True) #动态编号
    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #发布动态的用户编号
    aid = Column(ForeignKey(u'activities.aid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)   #与动态相关的活动编号
    time = Column(String(255))  #动态发布时间
    content = Column(String(255))   #动态内容
    access = Column(Integer, default=1)    #访问权限

    user = relationship(u'User')
    activity = relationship(u'Activity')

    def init_moment(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__


class MomentLike(Base):
    __tablename__ = 'moment_likes'

    mlid = Column(Integer, primary_key=True)    #动态点赞编号
    mid = Column(ForeignKey(u'moments.mid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)  #被点赞的动态编号
    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #点赞者的用户编号
    time = Column(String(255))  #点赞时间

    user = relationship(u'User')
    moment = relationship(u'Moment')


class MomentComment(Base):
    __tablename__ = 'moment_comments'

    cmid = Column(Integer, primary_key=True)    #动态评论编号
    mid = Column(ForeignKey(u'moments.mid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)  #被评论的动态编号
    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #评论者用户编号
    content = Column(String(255))   #评论内容
    time = Column(String(255))  #评论时间

    user = relationship(u'User')
    moment = relationship(u'Moment')

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__

class MomentImage(Base):
    __tablename__ = 'moment_images'

    imid = Column(Integer, primary_key=True)    #动态所包含的图片编号
    mid = Column(ForeignKey(u'moments.mid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)  #图片所属的动态编号
    md5 = Column(String(255))   #对应的图片文件名

    moment = relationship(u'Moment')

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__


class Corporation(Base):
    __tablename__ = 'corporation'

    cid = Column(Integer, primary_key=True)
    # userName = Column(String(255))
    # passWord = Column(String(255))
    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)    #团队用户编号
    slogan = Column(String(255))    #团队口号
    intro = Column(String(255)) #团队介绍
    name = Column(String(255))  #团队名称
    # thumbs = Column(Integer)    #点赞数量

    user = relationship(u'User')

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__
