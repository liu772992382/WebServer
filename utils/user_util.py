#!/usr/bin/env python
#coding=utf8

import sys
sys.path.append("..")
from model import *


def get_user(*args):
    tmp = {'status':False, 'data':[]}
    try:
        for i in args:
            print i
            tmp['data'].append(session.query(User).filter_by(openId=i).first().get_dict())
        tmp['status'] = True
        return tmp
    except Exception, e:
        print Exception, e
        tmp['info'] = 'No such user'
        return tmp

def get_all_user():
    tmp = {'status':False, 'data':[]}
    try:
        users = session.query(User).all()
        for i in users:
            tmp['data'].append(i.get_dict())
    except:
        pass
    finally:
        return tmp

def if_user_exist(open_id):
    tmp = {'status':False}
    tmp_user = session.query(User).filter_by(openId=open_id).all()
    if tmp_user != []:
        tmp['data'] = tmp_user
        tmp['status'] = True
        return tmp
    else:
        return tmp


def create_user(**kwargs):
    tmp = {'status':False}
    if not if_user_exist(kwargs['openId'])['status']:
        tmp_user = User()
        tmp_user.createTime = get_time()
        tmp_user.init_user(**kwargs)
        try:
            session.add(tmp_user)
            session.commit()
            tmp['status'] = True
            return tmp
        except:
            return tmp
    else:
        tmp['info'] = 'this user is existed!'
        return tmp

def update_user(**kwargs):
    tmp = {'status':False}
    print kwargs['openId']
    if if_user_exist(kwargs['openId'])['status']:
        tmp_user = session.query(User).filter_by(openId=kwargs['openId']).first()
        try:
            tmp_user.init_user(**kwargs)
            session.commit()
            tmp['status'] = True
            return tmp
        except:
            tmp['info'] = 'error'
            return tmp
    else:
        tmp['info'] = 'no such user'
        return tmp

def delete_user(open_id):
    tmp = {'status':False}

    tmp_users = if_user_exist(open_id)
    if tmp_users['status']:
        try:
            for i in tmp_users['data']:
                session.delete(i)
            session.commit()
            tmp['status'] = True
            return tmp
        except:
            return tmp
    else:
        tmp['info'] = 'no such user'
        return tmp


def login_user(open_id):
    tmp = {'status':False}
    tmp_user = session.query(User).filter_by(openId=open_id).first()
    if tmp_user:
        tmp_user.loginTime = get_time()
        session.commit()
        tmp['status'] = True
        return tmp
    else:
        return tmp
