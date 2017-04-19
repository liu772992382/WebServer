#!/usr/bin/env python
#coding=utf-8
#FKXXbLlfJpId
from os import urandom

SQLALCHEMY_DATABASE_URI='mysql://root:19951028liu@localhost:3306/web_api?charset=utf8'
SQLALCHEMY_COMMIT_ON_TEARDOWN=True
SQLALCHEMY_TRACK_MODIFICATIONS=True
SECRET_KEY = 'Shanyi'
#admin
ADMIN_USERNAME = 'Shanyi'
ADMIN_PASSWORD = 'ShanyiAdmin'

UPLOAD_FOLDER = 'images/upload'
HOST_PORT = 8081

QINIUURL = 'http://oo4l2ezdu.bkt.clouddn.com/'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
