# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer, SmallInteger, String, Table, Text, \
                       text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask import Flask
from config import *
import sys, os

engine = create_engine('mysql://root:19951028liu@localhost:3306/web_api?charset=utf8')

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    uid = Column(Integer, primary_key=True)
    openId = Column(String)
    nickName = Column(String)
    gender = Column(Integer)
    type = Column(Integer)
    loginTime = Column(String)



class Activity(Base):
    __tablename__ = 'activities'

    aid = Column(Integer, primary_key=True)
    name = Column(String)
    organizer = Column(String)
    time = Column(String)
    content = Column(String)
    summary = Column(String)


class Participant(Base):
    __tablename__ = 'participants'

    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    time = Column(String)

    user = relationship(u'User')


class Moment(Base):
    __tablename__ = 'moments'

    mid = Column(Integer, primary_key=True)
    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    aid = Column(ForeignKey(u'activities.aid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    time = Column(String)
    content = Column(String)
    access = Column(Integer)#访问权限

    user = relationship(u'User')
    activity = relationship(u'Activity')


class MomentLike(Base):
    __tablename__ = 'moment_likes'

    mid = Column(ForeignKey(u'moments.mid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    time = Column(String)

    user = relationship(u'User')
    moment = relationship(u'Moment')


class MomentComment(Base):
    __tablename__ = 'moment_comments'

    cmid = Column(Integer, primary_key=True)
    mid = Column(ForeignKey(u'moments.mid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    content = Column(String)
    time = Column(String)

    user = relationship(u'User')
    moment = relationship(u'Moment')


class MomentImage(Base):
    __tablename__ = 'moment_images'

    imid = Column(Integer, primary_key=True)
    mid = Column(ForeignKey(u'moments.mid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    md5 = Column(String)

    moment = relationship(u'Moment')
