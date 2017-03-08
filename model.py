# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer, SmallInteger, String, Table, Text, \
                       text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask import Flask
from config import *
import sys, os

engine = create_engine(SQLALCHEMY_DATABASE_URI)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    uid = Column(Integer, primary_key=True)
    openId = Column(String(255))
    nickName = Column(String(255))
    gender = Column(Integer)
    type = Column(Integer)
    loginTime = Column(String(255))



class Activity(Base):
    __tablename__ = 'activities'

    aid = Column(Integer, primary_key=True)
    name = Column(String(255))
    organizer = Column(String(255))
    time = Column(String(255))
    content = Column(String(255))
    summary = Column(String(255))


class Participant(Base):
    __tablename__ = 'participants'

    pid = Column(Integer, primary_key=True)
    uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    aid = Column(ForeignKey(u'activities.aid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    time = Column(String(255))

    user = relationship(u'User')
    activity = relationship(u'Activity')


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


class MomentImage(Base):
    __tablename__ = 'moment_images'

    imid = Column(Integer, primary_key=True)
    mid = Column(ForeignKey(u'moments.mid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    md5 = Column(String(255))

    moment = relationship(u'Moment')


# class Message(Base):
#     __tablename__ = 'messages'
#
#     msid = Column(Integer, primary_key=True)
#     uid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
#     fanUid = Column(ForeignKey(u'users.uid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
