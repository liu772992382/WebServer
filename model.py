# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer, SmallInteger, String, Table, Text, \
                       text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask import Flask
from config import *
import sys, os
import time

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker()
Session.configure(bind=engine)
Base = declarative_base()
session = Session()

def get_time():
    return time.strftime("%Y-%m-%d %X", time.localtime())



class User(Base):
    __tablename__ = 'users'

    uid = Column(Integer, primary_key=True)
    openId = Column(String(255))
    nickName = Column(String(255))
    gender = Column(Integer)
    type = Column(Integer)
    loginTime = Column(String(255))
    avatar = Column(String(255))
    createTime = Column(String(255))

    def init_user(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__



class Activity(Base):
    __tablename__ = 'activities'

    aid = Column(Integer, primary_key=True)
    name = Column(String(255))
    organizer = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    time = Column(String(255))
    content = Column(String(255))
    summary = Column(String(255))

    def init_activity(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__

class Participant(Base):
    __tablename__ = 'participants'

    pid = Column(Integer, primary_key=True)
    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    aid = Column(ForeignKey(u'activities.aid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    time = Column(String(255))

    user = relationship(u'User')
    activity = relationship(u'Activity')

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__

class Moment(Base):
    __tablename__ = 'moments'

    mid = Column(Integer, primary_key=True)
    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    aid = Column(ForeignKey(u'activities.aid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    time = Column(String(255))
    content = Column(String(255))
    access = Column(Integer)#访问权限

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

    mlid = Column(Integer, primary_key=True)
    mid = Column(ForeignKey(u'moments.mid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    time = Column(String(255))

    user = relationship(u'User')
    moment = relationship(u'Moment')


class MomentComment(Base):
    __tablename__ = 'moment_comments'

    cmid = Column(Integer, primary_key=True)
    mid = Column(ForeignKey(u'moments.mid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    content = Column(String(255))
    time = Column(String(255))

    user = relationship(u'User')
    moment = relationship(u'Moment')

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__

class MomentImage(Base):
    __tablename__ = 'moment_images'

    imid = Column(Integer, primary_key=True)
    mid = Column(ForeignKey(u'moments.mid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    md5 = Column(String(255))

    moment = relationship(u'Moment')

    def get_dict(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__

# class Message(Base):
#     __tablename__ = 'messages'
#
#     msid = Column(Integer, primary_key=True)
#     uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
#     fanUid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
